<?php
class PostModel extends Db
{
    public function getAllData(){
        $con = $this->conn;
        $result = $con->query("SELECT * FROM Post");
        $posts = array();
        if ($result-> num_rows > 0)
        {
            while ($post = mysqli_fetch_assoc($result)){
                $posts[]=$post;
            }
        }
        return $posts;
    }
    public function addData($params=[])
    {
        if (trim($params[0]) != "")
        {
            $time = date('Y/m/d H:i:s');
            if ($params[2] != '/images/')
            {
                $sql = "INSERT INTO Post (title, description, image, status, create_at) VALUE ('$params[0]', '$params[1]', '$params[2]', '$params[3]','$time')";
            }
            else
            {
                $sql = "INSERT INTO Post (title, description, status, create_at) VALUE ('$params[0]', '$params[1]', '$params[3]','$time')";
            }
            mysqli_query($this->conn, $sql);
        }
    }
    public function getOneData($id){
        $con = $this->conn;
        $result = $con->query("SELECT * FROM Post WHERE id =$id");
        $posts = array();
        if ($result-> num_rows > 0)
        {
            while ($post = mysqli_fetch_assoc($result)){
                $posts[]=$post;
            }
        }
        return $posts;
    }
    public function removeData($param)
    {
        if (is_numeric($param))
        {
            $sql = "DELETE FROM Post WHERE id=$param";
            mysqli_query($this->conn, $sql);
            return header("Location: /train2/Admin/Show", true, 301);
            exit();
        }
    }
    public function editData($param)
    {
        if (is_numeric($param[0]))
        {
            $time = date('Y/m/d H:i:s');
            if ($param[3] != '')
            {
                $sql = "UPDATE Post SET title = '$param[1]', description='$param[2]', image='$param[3]', status='$param[4]', update_at='$time' WHERE id=$param[0]";
            }
            else
            {
                $sql = "UPDATE Post SET title='$param[1]', description='$param[2]', status='$param[4]', update_at='$time' WHERE id=$param[0]";
            }
            if (mysqli_query($this->conn, $sql))
            {}
            else
            {
                echo "ERROR: Could not able to execute $sql. " .mysqli_error($link);
            }
        }
    }
}

?>
