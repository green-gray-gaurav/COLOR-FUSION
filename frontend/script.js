var base_image_output = document.getElementById("base_image_output");
var input_image_output = document.getElementById("input_image_output");
var fusion_image = document.getElementById("fusion_image");

var base_image = null;
var input_image = null;
var fused_image = null;

var clusters = 10;
var alpha = 0.01;
var beta = 0.01;
var enchant = 0.8;
var shift = 0.3;

var version = "version1";

const url = "http://127.0.0.1:5000/fuse";
const url_use_color = "http://127.0.0.1:5000/use";

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

function hide_slider_all() {
  var sliders = ["cluster", "alpha", "beta", "enchant", "shift"];
  sliders.forEach((value, idx) => {
    var elm = document.getElementById(value + "_slider_container");
    console.log(elm);
    elm.classList.add("deactivate_elm");
  });
}
function show_slider(list) {
  list.forEach((value, idx) => {
    var elm = document.getElementById(value + "_slider_container");
    console.log(elm);
    elm.classList.remove("deactivate_elm");
  });
}

hide_slider_all();

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
  if (idx == 3) {
    document.getElementById("enchant_range").innerHTML = elm.value / 10;
    enchnat = elm.value / 10;
  }
  if (idx == 4) {
    document.getElementById("shift_range").innerHTML = elm.value / 10;
    shift = elm.value / 10;
  }
}

function drop_down(obj) {
  version = obj.value;
  if (version == "version1") {
    hide_slider_all();
    show_slider(["cluster", "alpha", "beta"]);
  }
  if (version == "version2") {
    hide_slider_all();
    show_slider(["cluster", "enchant"]);
  }
  if (version == "version3") {
    hide_slider_all();
    show_slider(["cluster", "enchant", "shift"]);
  }
}

async function fuse_images(obj, compute = true) {
  if (!base_image || !input_image) {
    alert("please upload the images");
    return;
  }

  obj.innerHTML = compute ? "FUSING..." : "USING...";
  obj.style.backgroundColor = "blue";

  var data = {
    image1: base_image,
    image2: input_image,
    clusters: clusters,
    alpha: alpha,
    beta: beta,
    enchant: enchant,
    shift: shift,
    version: version,
    compute: compute,
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

      obj.innerHTML = compute ? "FUSE" : "USE";
      obj.style.backgroundColor = "black";
    });
}
