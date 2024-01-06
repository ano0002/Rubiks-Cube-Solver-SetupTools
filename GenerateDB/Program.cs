using System.ComponentModel.DataAnnotations;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text.Json;
using System.Text.Json.Serialization;

class Generator{
    public static void Main(String[] args){
        CornerCube cube = new CornerCube();
        Queue<CornerCube> queue = new Queue<CornerCube>(); 
        queue.Enqueue(cube);
        Dictionary<string, byte> cornerDict = new Dictionary<string, byte>();
        BFS(queue, ref cornerDict);
        string json = JsonSerializer.Serialize(cornerDict);
        File.WriteAllText(@"C:\Users\recke\OneDrive - Hills Road Sixth Form College\Computer Science\NEA Retry\Rubiks-Cube-Solver\GenerateDB\cornerDict.json", json);
    }

    public static void BFS(Queue<CornerCube> queue, ref Dictionary<string, byte> dict){
        byte depth = 0;
        long timeStamp = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
        while (queue.Count() != 0){
            System.Console.WriteLine("DEPTH REACHED: " + depth);
            System.Console.WriteLine("Total time elapsed: " + (DateTimeOffset.UtcNow.ToUnixTimeSeconds()-timeStamp) + "s");
            int layerSize = queue.Count();
            while (layerSize != 0){
                CornerCube cube = queue.Dequeue();
                string key = cube.generateKey();
                if (!dict.ContainsKey(key)){
                    dict.Add(key, depth);
                    for (int i = 0; i < 2; i++){
                        for (int j = 0; j < 6; j++){
                            CornerCube newCube = new CornerCube(cube.getState());
                            if(i == 0){
                                newCube.rotateFace(j, 1);
                            }else{
                                newCube.rotateFace(j, -1);
                            }
                            queue.Enqueue(newCube);
                        }
                    }
                }
                layerSize--;
            }
            depth++;
        }
    }
}