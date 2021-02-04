<div style="margin-top: 10px" class="container">
    <?php foreach ($data['data'] as $post) : ?>
        <div class="row">
            <h3 class="col-10"><?php echo $post['title'];?></h3>
            <a type="button" href="http://localhost/train2/Admin" class="editBtn btn btn-primary col-1"
               class="btn btn-primary">Back</a>
        </div>
        <hr/>
        <div class="row">
            <img class="col-4" src="../../public/images/<?php echo $post['image'];?>" height="160">
            <p class="col-8"><?php echo $post['description']?></p>
        </div>
    <?php endforeach; ?>
</div>

