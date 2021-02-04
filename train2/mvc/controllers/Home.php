<?php
class Home extends Controller
{
    function Show()
    {
        $data = $this->model("PostModel");
        $post = $data->getAllData();
        $this->view("layout", ["page"=>"Home", "data"=>$post]);
    }
    function Detail($id)
    {
        $data = $this->model("PostModel");
        $post = $data->getOneData($id);
        $this->view("layout", ["page"=>"ShowOne", "data"=>$post]);
    }

}

?>
