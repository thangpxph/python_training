<div class="container">
    <div class="row">
        <h3 class="col-10">ADD</h3>
        <div class="row col-2">
            <a type="button" href="http://localhost/train2/Admin" class="editBtn btn btn-ligh col-1"
               class="btn btn-primary">Back</a>
        </div>
    </div>
    <hr/>
    <form action="Add" method="post" enctype="multipart/form-data">
        <div class="row">
            <label class="col-3">Title</label>
            <input type="text" class="form-control col-9" name="title" placeholder="Title">
        </div>
        <hr/>
        <div class="row">
            <label class="col-3">Description</label>
            <textarea class="form-control col-9" name="description" placeholder="Description" rows="4"></textarea>
        </div>
        <br/>
        <div class="row">
            <label class="col-3" for="customFile">Image</label>
            <div class="custom-file col-9">
                <input type="file" name="image" class="custom-file-input" id="customFile">
                <label class="custom-file-label" for="customFile">Choose file</label>
            </div>
            <br/>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
            <img  style="display: none;margin-left: 20px" id="blah" src="#" alt="your image" width="200" height="160"/>
        </div>
        <hr/>
        <div class="row">
            <label class="col-3" for="status_select">Status</label>
            <div class="form-group col-9">
                <select name="status" class="form-control" id="status_select">
                    <option>Enable</option>
                    <option>Disable</option>
                </select>
            </div>
        </div>
        <button type="submit" class="btn btn-primary">Save</button>
    </form>
</div>
<script>
    $(".custom-file-input").on("change", function () {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#blah').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]); // convert to base64 string
        }
    }

    $("#customFile").change(function () {
        readURL(this);
        $('#blah').css("display", "block");
    });
</script>
