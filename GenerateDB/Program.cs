class CornerCube{
    public CornerCube(){
        int[][][] corners = new int[6][][];
        for (int i = 0; i < corners.Length; i++)
        {
            corners[i] = new int[2][];
            for (int j = 0; j < corners[i].Length; j++)
            {
                corners[i][j] = new int[2];
            }
        }
    }

    public void rotateFace(int face, int dir){
        
    }
}