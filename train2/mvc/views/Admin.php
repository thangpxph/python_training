<div class="container">
    <div class="row">
        <div class="col-md-12">
            <h3>Admin</h3>
            <!-- Button trigger modal -->
            <a style="margin-left: 90%"  type="button" class="btn btn-primary" href="http://localhost/train2/Admin/Add">
                Add
            </a>
            <hr/>
            <table style="text-align: center" class="table table-striped table-hover table-bordered" id="tbpost">
                <thead>
                <tr>
                    <th style="width: 10%">#</th>
                    <th style="width: 15%">Thumb</th>
                    <th style="width: 45%">Title</th>
                    <th style="width: 10%">Status</th>
                    <th style="width: 20%">Action</th>
                </tr>
                </thead>
                <tbody id="tbody">
                <?php foreach ($data['data'] as $post) : ?>
                <tr>
                    <td><?php echo $post['id']; ?></td>
                    <td><img src="./public/images/<?php echo $post['image']?>" width="100", height="100" ></td>
                    <td><?php echo $post['title'];?></td>
                    <td>
                        <?php if ($post['status'] == 0){
                            echo 'Enable';
                        }else{echo 'Disable';} ?>
                    </td>
                    <td>
                        <div style="margin-left: 2px" class="row">
                            <a type="button" href="http://localhost/train2/Admin/detail/<?php echo $post['id']?>" class="editBtn btn btn-primary"
                                    class="btn btn-primary">Show
                            </a>
                            <a type="button" href="http://localhost/train2/Admin/edit/<?php echo $post['id']?>" class="editBtn btn btn-primary"
                                    class="btn btn-primary">Edit
                            </a>
                            <button type="button" name="deleteBtn" class="deleteBtn btn btn-danger" data-id=<?php echo $post['id']?>
                                class="btn btn-danger">Delete
                            </button>
                        </div>
                    </td>
                </tr>
                <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
    <div class="modal fade" id="deleteId" tabindex="-1" role="dialog" aria-labelledby="deleteTitleId"
         aria-hidden="true">
        <div class="modal-dialog" role="document">
            <form action="/admin/category/delete" method="post">
                <input type="hidden" name="categoryIdDel" id="categoryIdDel">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="headingDel">Xóa thể loại</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <h6>Bạn muốn xóa thể loại và tất cả món ăn trong thể loại này</h6>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Huỷ</button>
                        <button type="submit" id="submitBtn" class="btn btn-primary">Xóa</button>
                    </div>
                </div>
            </form>
        </div>
</div>
<script>
    function delEvent(){
        document.querySelectorAll('.deleteBtn').forEach(item => {
            item.addEventListener('click', e =>{
                let pid = e.target.dataset.id;
                document.querySelector('#categoryIdDel').value = pid;
                location.href = "/train2/Admin/drop/" + pid;
                $('#deleteId').modal('show')
            })
        })
    }
    delEvent();
    $('#tbpost').DataTable();
</script>

