Webcam.set({
    width: 450,
    height: 450,
    image_format: 'jpeg',
    jpeg_quality: 100
});
Webcam.attach('#camera');

// SHOW THE SNAPSHOT.
takeSnapShot = function () {
    Webcam.snap(function (data_uri) {
        downloadImage('download', data_uri);
    });
}

downloadImage = function (name, datauri) {
    var a = document.createElement('a');
    a.setAttribute('download', name + '.jpeg');
    a.setAttribute('href', datauri);
    a.click();
}

$("#utPic").click(function(){
    $("#files").click()
    $("#files").val('')
})

$("#files").change(function(){
    $("#uploadFile").submit()
})