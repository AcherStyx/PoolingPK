<template>
  <div>
    <!--main canvas-->
    <canvas id="myCanvas" width="300" height="300"></canvas>
  </div>
  <div>
    <!--log output-->
    <p id="key_log"></p>
    <p>Environment status response: </p>
    <p id="env_response"></p>
  </div>
</template>

<script>
export default {
  name: "PoolingPK",
  mounted() {

    let move_up = false;
    let move_down = false;
    let move_left = false;
    let move_right = false;

    const log = document.getElementById('key_log');
    const env_log = document.getElementById("env_response")

    env_log.textContent = `Environment status response: None`;


    // const input = document.querySelector('input');
    document.addEventListener('keydown', KeyDown, false);
    document.addEventListener('keyup', KeyUp, false)


    function KeyDown(e) {
      e.preventDefault();
      log.textContent = ` ${e.code}`;

      if (e.code == "KeyA") {
        move_left = true;
      } else if (e.code == "KeyD") {
        move_right = true;
      } else if (e.code == "KeyW") {
        move_up = true;
      } else if (e.code == "KeyS") {
        move_down = true;
      }
    }

    function KeyUp(e) {
      e.preventDefault();

      if (e.code == "KeyA") {
        move_left = false;
      } else if (e.code == "KeyD") {
        move_right = false;
      } else if (e.code == "KeyW") {
        move_up = false;
      } else if (e.code == "KeyS") {
        move_down = false;
      }
    }

    var x = 150;
    var y = 150;
    var step = 2;

    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");

    async function draw() {
      async function get_env_status() {
        const requestOptions = {
          method: 'GET',
          redirect: 'follow'
        };
        return fetch("http://localhost:8000/pooling_pk/0/get_status", requestOptions)
            .then(response => response.json())
            .then(responseJson => {
              return responseJson
            })
            .catch(error => console.log('error', error));
      }

      function draw_gamer(gamer) {
        ctx.beginPath();
        ctx.arc(gamer.x, gamer.y, 10, 0, 2 * Math.PI);
        ctx.stroke();
      }

      const env_status = await get_env_status();
      env_log.textContent = `${JSON.stringify(env_status)}`;

      ctx.clearRect(0, 0, 300, 300);
      ctx.beginPath();

      if (move_up) {
        y -= step
      }
      if (move_down) {
        y += step
      }
      if (move_left) {
        x -= step
      }
      if (move_right) {
        x += step
      }
      ctx.arc(x, y, 10, 0, 2 * Math.PI);
      ctx.stroke();

      for (var idx in env_status["gamer"]) {
        const gamer = env_status["gamer"][idx];
        draw_gamer(gamer)
      }

    }

    function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function run() {
      draw();
      await sleep(10);
      window.requestAnimationFrame(run);
    }

    run();
  }
}


</script>

<style scoped>
canvas {
  border: 1px solid lightgray;
}

p {
  color: gray;
  text-align: left;
}

</style>