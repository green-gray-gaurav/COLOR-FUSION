var base_image_output = document.getElementById("base_image_output");
var input_image_output = document.getElementById("input_image_output");
var fusion_image = document.getElementById("fusion_image");

var base_image = null;
var input_image = null;
var fused_image = null;

var clusters = 10;
var alpha = 0.01;
var beta = 0.01;

const url = "http://127.0.0.1:5000/fuse";

function readURL(idx, input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      if (idx == 1) {
        base_image_output.setAttribute("src", e.target.result);
        base_image = e.target.result;
      } else if (idx == 2) {
        input_image_output.setAttribute("src", e.target.result);
        input_image = e.target.result;
      }
    };
    reader.readAsDataURL(input.files[0]);
  }
}

function slider(idx, elm) {
  if (idx == 0) {
    document.getElementById("cluster_range").innerHTML = elm.value;
    clusters = elm.value;
  }
  if (idx == 1) {
    document.getElementById("alpha_range").innerHTML = elm.value / 1000;
    alpha = elm.value / 1000;
  }
  if (idx == 2) {
    document.getElementById("beta_range").innerHTML = elm.value / 1000;
    beta = elm.value / 1000;
  }
}

async function fuse_images() {
  if (!base_image || !input_image) {
    alert("please upload the images");
    return;
  }

  document.getElementById("fuse_button").innerHTML = "FUSING...";
  document.getElementById("fuse_button").style.backgroundColor = "red";
  var data = {
    image1: base_image,
    image2: input_image,
    clusters: clusters,
    alpha: alpha,
    beta: beta,
  };

  var options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  };

  fetch(url, options)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.blob();
    })
    .then((value) => {
      console.log(value);
      fused_image = URL.createObjectURL(value);
      fusion_image.setAttribute("src", fused_image);
      document
        .getElementById("download_image")
        .setAttribute("href", fused_image);
      document
        .getElementById("download_image")
        .classList.remove("invisible_elm");

      document.getElementById("fuse_button").innerHTML = "FUSE";
      document.getElementById("fuse_button").style.backgroundColor = "black";
    });
}
