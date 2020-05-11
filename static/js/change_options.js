function ch(options){
    var content='<option value="default-cate">请选择所属课程分类：</option>';
    var selected=$('[name="course_sel"] option:selected').val();
    for (var i=0;i<options.length;i++){
        if (options[i].cid===selected){
            content+='<option value="'+options[i].id+'">'+options[i].name+'</option>';
        }
    }
    $('[name="cate_sel"]').html(content);
}