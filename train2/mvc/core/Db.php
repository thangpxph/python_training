<?php
class Db
{
    public $conn;
    protected $servername = "localhost";
    protected $username = "root";
    protected $password = "admin123";
    protected $dbname = "train2";

    function __construct()
    {
        $this->conn = mysqli_connect($this->servername, $this->username, $this->password);
        if ($this->conn === false)
        {
            die("ERROR: Could not connect. " .mysqli_connect_error());
        }
        else
        {
            mysqli_select_db($this->conn, $this->dbname);
            mysqli_query($this->conn, "SET NAME 'utf8mb4'");
        }
    }

}

?>
