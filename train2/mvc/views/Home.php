<div class="container">
    <div class="row">
        <div class="col-md-12">
            <h3>Home</h3>
            <hr/>
            <table style="text-align: center" class="table table-striped table-hover table-bordered" id="tbcategory">
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
                        <td>
                            <a style="color: aliceblue" type="button" href="http://localhost/train2/Home/Detail/<?php echo $post['id'] ?>" class="editBtn btn btn-primary"
                                    class="btn btn-primary">Show</a>
                        </td>
                    </tr>
                <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<script>
    $('#tbcategory').DataTable();
</script>