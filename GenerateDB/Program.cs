class Generator{
    public static void Main(String[] args){
        CornerCube cube = new CornerCube();
        cube.rotateFace(5,1);
        System.Console.WriteLine(cube);
    }
}