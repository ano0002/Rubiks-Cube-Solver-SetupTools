class CornerCube{
    private int[,,] corners;
    public CornerCube(){
        this.corners = new int[6,2,2];
        for (int i = 0; i < 6; i++)
        {
            for (int j = 0; j < 2; j++)
            {
                corners[i,j,0] = i;
                corners[i,j,1] = i;
            }
        }
    }

    public string generateKey(){
        string output = "";
        for (int i = 0; i < corners.GetLength(0); i++){
            for (int j = 0; j < corners.GetLength(1); j++){
                for (int k = 0; k < corners.GetLength(2); k++){
                    output += corners[i,j,k];
                }
            }
        }
        return output;
    }

    public override string ToString()
    {
        string output = "";
        for (int i = 0; i < corners.GetLength(0); i++){
            for (int j = 0; j < corners.GetLength(1); j++){
                for (int k = 0; k < corners.GetLength(2); k++){
                    output += corners[i,j,k];
                }
                output += "\n";
            }
        }
        return output;
    }

    public void rotateFace(int face, int dir){
        int[,,] newCube = new int[6,2,2];
        Array.Copy(this.corners, newCube, 24);
        if (dir == 1){ // Anti-Clockwise
            newCube[face,0,0] = this.corners[face,0,1];
            newCube[face,0,1] = this.corners[face,1,1];
            newCube[face,1,1] = this.corners[face,1,0];
            newCube[face,1,0] = this.corners[face,0,0];
        }else{ // Clockwise
            newCube[face,0,0] = this.corners[face,1,0];
            newCube[face,0,1] = this.corners[face,0,0];
            newCube[face,1,1] = this.corners[face,0,1];
            newCube[face,1,0] = this.corners[face,1,1];
        }
        if (dir == 1){ // AC
            if(face == 0){
                newCube[3,0,1] = this.corners[2,0,1];
                newCube[3,0,0] = this.corners[2,0,0];
                newCube[2,0,1] = this.corners[1,0,1];
                newCube[2,0,0] = this.corners[1,0,0];
                newCube[1,0,1] = this.corners[4,0,1];
                newCube[1,0,0] = this.corners[4,0,0];
                newCube[4,0,1] = this.corners[3,0,1];
                newCube[4,0,0] = this.corners[3,0,0];
            }else if(face == 1){
                newCube[0,1,0] = this.corners[2,0,0];
                newCube[0,1,1] = this.corners[2,1,0];
                newCube[2,0,0] = this.corners[5,0,1];
                newCube[2,1,0] = this.corners[5,0,0];
                newCube[5,0,1] = this.corners[4,1,1];
                newCube[5,0,0] = this.corners[4,0,1];
                newCube[4,1,1] = this.corners[0,1,0];
                newCube[4,0,1] = this.corners[0,1,1];
            }else if(face == 2){
                newCube[0,1,1] = this.corners[3,0,0];
                newCube[0,0,1] = this.corners[3,1,0];
                newCube[3,0,0] = this.corners[5,1,1];
                newCube[3,1,0] = this.corners[5,0,1];
                newCube[5,1,1] = this.corners[1,1,1];
                newCube[5,0,1] = this.corners[1,0,1];
                newCube[1,1,1] = this.corners[0,1,1];
                newCube[1,0,1] = this.corners[0,0,1];
            }else if (face == 3){
                newCube[0,0,0] = this.corners[4,1,0];
                newCube[0,0,1] = this.corners[4,0,0];
                newCube[2,0,1] = this.corners[0,0,0];
                newCube[2,1,1] = this.corners[0,0,1];
                newCube[5,1,1] = this.corners[2,0,1];
                newCube[5,1,0] = this.corners[2,1,1];
                newCube[4,1,0] = this.corners[5,1,1];
                newCube[4,0,0] = this.corners[5,1,0];
            }else if(face == 4){
                newCube[0,1,0] = this.corners[1,1,0];
                newCube[0,0,0] = this.corners[1,0,0];
                newCube[3,0,1] = this.corners[0,1,0];
                newCube[3,1,1] = this.corners[0,0,0];
                newCube[5,1,0] = this.corners[3,0,1];
                newCube[5,0,0] = this.corners[3,1,1];
                newCube[1,1,0] = this.corners[5,1,0];
                newCube[1,0,0] = this.corners[5,0,0];
            }else if(face == 5){
                newCube[1,1,0] = this.corners[2,1,0];
                newCube[1,1,1] = this.corners[2,1,1];
                newCube[2,1,0] = this.corners[3,1,0];
                newCube[2,1,1] = this.corners[3,1,1];
                newCube[3,1,0] = this.corners[4,1,0];
                newCube[3,1,1] = this.corners[4,1,1];
                newCube[4,1,0] = this.corners[1,1,0];
                newCube[4,1,1] = this.corners[1,1,1];
            }
        }else{ // C
            if(face == 0){
                newCube[3,0,1] = this.corners[4,0,1];
                newCube[3,0,0] = this.corners[4,0,0];
                newCube[2,0,1] = this.corners[3,0,1];
                newCube[2,0,0] = this.corners[3,0,0];
                newCube[1,0,1] = this.corners[2,0,1];
                newCube[1,0,0] = this.corners[2,0,0];
                newCube[4,0,1] = this.corners[1,0,1];
                newCube[4,0,0] = this.corners[1,0,0];
            }else if(face == 1){
                newCube[0,1,0] = this.corners[4,1,1];
                newCube[0,1,1] = this.corners[4,0,1];
                newCube[2,0,0] = this.corners[0,1,0];
                newCube[2,1,0] = this.corners[0,1,1];
                newCube[5,0,1] = this.corners[2,0,0];
                newCube[5,0,0] = this.corners[2,1,0];
                newCube[4,1,1] = this.corners[5,0,1];
                newCube[4,0,1] = this.corners[5,0,0];
            }else if(face == 2){
                newCube[0,1,1] = this.corners[1,1,1];
                newCube[0,0,1] = this.corners[1,0,1];
                newCube[3,0,0] = this.corners[0,1,1];
                newCube[3,1,0] = this.corners[0,0,1];
                newCube[5,1,1] = this.corners[3,0,0];
                newCube[5,0,1] = this.corners[3,1,0];
                newCube[1,1,1] = this.corners[5,1,1];
                newCube[1,0,1] = this.corners[5,0,1];
            }else if (face == 3){
                newCube[0,0,0] = this.corners[2,0,1];
                newCube[0,0,1] = this.corners[2,1,1];
                newCube[2,0,1] = this.corners[5,1,1];
                newCube[2,1,1] = this.corners[5,1,0];
                newCube[5,1,1] = this.corners[4,1,0];
                newCube[5,1,0] = this.corners[4,0,0];
                newCube[4,1,0] = this.corners[0,0,0];
                newCube[4,0,0] = this.corners[0,0,1];
            }else if(face == 4){
                newCube[0,1,0] = this.corners[3,0,1];
                newCube[0,0,0] = this.corners[3,1,1];
                newCube[3,0,1] = this.corners[5,1,0];
                newCube[3,1,1] = this.corners[5,0,0];
                newCube[5,1,0] = this.corners[1,1,0];
                newCube[5,0,0] = this.corners[1,0,0];
                newCube[1,1,0] = this.corners[0,1,0];
                newCube[1,0,0] = this.corners[0,0,0];
            }else if(face == 5){
                newCube[1,1,0] = this.corners[4,1,0];
                newCube[1,1,1] = this.corners[4,1,1];
                newCube[2,1,0] = this.corners[1,1,0];
                newCube[2,1,1] = this.corners[1,1,1];
                newCube[3,1,0] = this.corners[2,1,0];
                newCube[3,1,1] = this.corners[2,1,1];
                newCube[4,1,0] = this.corners[3,1,0];
                newCube[4,1,1] = this.corners[3,1,1];
            }
        }
        this.corners = newCube;
    }

}

class Generator{
    public static void Main(String[] args){
        CornerCube cube = new CornerCube();
        System.Console.WriteLine(cube);
        cube.rotateFace(1,1);
        System.Console.WriteLine(cube);
    }
}