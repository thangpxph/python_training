<?php
class Admin extends Controller
{
    function Show()
    {
        $data = $this->model("PostModel");
        $post = $data->getAllData();
        $this->view(layout, ["page" => "Admin", "data" => $post]);
    }

    function detail($id)
    {
        $data = $this->model("PostModel");
        $post = $data->getOneData($id);
        $this->view("layout", ["page" => "showad", "data" => $post]);
    }

    function Add()
    {
        $this->view("layout", ["page" => "New"]);
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            if (isset($_FILES['image'])) {
                $errors = array();
                $file_name = $_FILES['image']['name'];
                $file_size = $_FILES['image']['size'];
                $file_tmp = $_FILES['image']['tmp_name'];
                $file_type = $_FILES['image']['type'];
                $file_ext = strtolower(end(explode('.', $_FILES['image']['name'])));
                $expensions = array("jpeg", "jpg", "png");

                if (in_array($file_ext, $expensions) === false) {
                    $errors[] = "extension not allowed, please choose a JPEG or PNG file.";
                }

                if ($file_size > 2097152) {
                    $errors[] = 'File size must be excately 2 MB';
                }

                if (empty($errors) == true) {
                    move_uploaded_file($file_tmp, "./public/images/" . $file_name);
                }
            }
            $title = $_POST['title'];
            $description = $_POST['description'];
            $image = $_FILES['image']['name'];
            if ($_POST['status'] == 'Disable') {
                $status = 0;
            } else {
                $status = 1;
            }
            $post = $this->model("PostModel");
            $post->addData([$title, $description, $image, $status]);
        }

    }

    function edit($id)
    {
        $data = $this->model("PostModel");
        $post = $data->getOneData($id);
        $this->view("layout", ["page" => "edit", "data" => $post]);
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            if (isset($_FILES['image'])) {
                $errors = array();
                $file_name = $_FILES['image']['name'];
                $file_size = $_FILES['image']['size'];
                $file_tmp = $_FILES['image']['tmp_name'];
                $file_type = $_FILES['image']['type'];
                $file_ext = strtolower(end(explode('.', $_FILES['image']['name'])));

                $expensions = array("jpeg", "jpg", "png");

                if (in_array($file_ext, $expensions) === false) {
                    $errors[] = "extension not allowed, please choose a JPEG or PNG file.";
                }

                if ($file_size > 2097152) {
                    $errors[] = 'File size must be excately 2 MB';
                }

                if (empty($errors) == true) {
                    move_uploaded_file($file_tmp, $file_name);
                }
            }
            $title = $_POST['title'];
            $description = $_POST['description'];
            $image = $_FILES['image']['name'];
            if ($_POST['status'] == 'Enable') {
                $status = 0;
            } else {
                $status = 1;
            }
            $product = $this->model("PostModel");
            $product->editData([$id, $title, $description, $image, $status]);
        }
        $data = $this->model("PostModel");
        $post = $data->getOneData($id);
        $this->view("layout", ["page" => "edit", "data" => $post]);

    }
    public function drop($id){
        $product = $this->model("PostModel");
        $product->removeData($id);
    }
}

?>
