<template>

  <div class="app">
    <div style="float:left;">
      <!--main canvas-->
      <canvas id="myCanvas" width="800" height="600"></canvas>
    </div>

    <div style="float:left;margin-left:10px;margin-right: 10px">
      <div id="notice" style="margin-left:10px;margin-right: 10px;">
        <div style="float: left">
          <p style="margin-top: 2px">Move:</p>
        </div>
        <div style="float: left; margin-left: 10px">
          <p id="move_key" style="margin-left: 30px">W</p>
          <p id="move_key" style="display:inline-block">A</p>
          <p id="move_key" style="display:inline-block">S</p>
          <p id="move_key" style="display:inline-block">D</p>
        </div>
        <div style="float: left; margin-left: 10px">
          <p style="margin-top: 2px">Attack:</p>
        </div>
        <div style="float: left; margin-left: 10px">
          <p style="border-radius: 5px; border: 2px solid lightgray; width: 100px; text-align: center; margin-top: 30px;">
            Space</p>
        </div>
      </div>
      <pre id="response"></pre>
    </div>
    <p id="key_log" style="display: none"></p>
  </div>


</template>

<script>
export default {
  name: "PoolingPK",
  mounted() {

    // hyper parameters
    const CANVAS_WIDTH = 800;
    const CANVAS_HEIGHT = 600;
    const FPS = 30;

    // player control
    let move_up = false;
    let move_down = false;
    let move_left = false;
    let move_right = false;
    let move_direction = 2;
    let fire = false;

    const log = document.getElementById('key_log');
    // const input = document.querySelector('input');
    document.addEventListener('keydown', KeyDown, false);
    document.addEventListener('keyup', KeyUp, false);

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
      } else if (e.code == "Space") {
        fire = true;
      } else if (e.code == "KeyR") {
        // restart
        const requestOptions = {
          method: 'GET',
          redirect: 'follow'
        };
        fetch("http://localhost:8000/pooling_pk/0/restart", requestOptions)
            .then(response => response.json())
            .then(responseJson => {
              return responseJson
            })
            .catch(error => console.log('error', error));
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
      } else if (e.code == "Space") {
        fire = false;
      }
    }

    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    ctx.imageSmoothingEnabled = false;


    async function draw() {
      // eslint-disable-next-line no-unused-vars
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

      function control(direction) {
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        var raw = JSON.stringify({
          "0": direction,
          "fire": fire
        });
        var requestOptions = {
          method: 'POST',
          headers: myHeaders,
          body: raw,
          redirect: 'follow'
        };
        return fetch("http://localhost:8000/pooling_pk/0/control", requestOptions)
            .then(response => response.json())
            .then(responseJson => {
              return responseJson
            })
            .catch(error => console.log('error', error));
      }

      async function draw_player(gamer) {
        var img = new Image();
        if (gamer.uid == 0)
          img.src = "player-red_10x.png";
        else
          img.src = "player-blue_10x.png";
        ctx.save()
        ctx.translate(gamer.x, gamer.y)
        ctx.rotate(Math.PI * -gamer.move_direction / 4)
        ctx.translate(-22, -25)
        ctx.drawImage(img, 0, 0, 55, 50)
        ctx.restore()
        // health bar
        ctx.fillStyle = "rgb(255,255,255)";
        ctx.fillRect(gamer.x - 20, gamer.y - 35, 100 * 0.4, 5)
        ctx.fillStyle = "rgb(255,0,0)";
        ctx.fillRect(gamer.x - 20, gamer.y - 35, gamer.health * 0.4, 5)
        if (gamer.health == 0) {
          ctx.fillStyle = "rgb(255,255,255)";
          for (var i = 0; i < 40; i++) {
            ctx.fillRect(gamer.x - 25 + Math.random() * 50, gamer.y - 25 + Math.random() * 50,
                1 + Math.random() * 5, 1 + Math.random() * 5);
          }
        }
      }

      async function draw_bullet(bullet) {
        if (bullet.health > 0) {
          var img = new Image();
          img.src = "bullet.png";
          ctx.save()
          ctx.translate(bullet.x, bullet.y)
          ctx.rotate(Math.PI * -bullet.move_direction / 4)
          ctx.translate(-7, -5)
          ctx.drawImage(img, 0, 0, 14, 10)
          ctx.fillStyle = "rgb(255,255,255)";
          for (let i = 0; i < 5; i++) {
            ctx.fillRect(-3 - Math.random() * 15, 0 + Math.random() * 5,
                1 + Math.random() * 5, 1 + Math.random() * 5);
          }
          ctx.restore()
        } else {
          ctx.fillStyle = "rgb(255,255,255)";
          for (let i = 0; i < 20; i++) {
            ctx.fillRect(bullet.x - 10 + Math.random() * 20, bullet.y - 10 + Math.random() * 20,
                1 + Math.random() * 3, 1 + Math.random() * 3);
          }
        }
      }

      if (!move_left && move_right && !move_up && !move_down)
        move_direction = 0
      else if (!move_left && move_right && move_up && !move_down)
        move_direction = 1
      else if (!move_left && !move_right && move_up && !move_down)
        move_direction = 2
      else if (move_left && !move_right && move_up && !move_down)
        move_direction = 3
      else if (move_left && !move_right && !move_up && !move_down)
        move_direction = 4
      else if (move_left && !move_right && !move_up && move_down)
        move_direction = 5
      else if (!move_left && !move_right && !move_up && move_down)
        move_direction = 6
      else if (!move_left && move_right && !move_up && move_down)
        move_direction = 7
      else
        move_direction = 8

      const env_status = await control(move_direction);

      const response_visualize = document.getElementById("response");
      response_visualize.innerHTML = JSON.stringify(env_status, undefined, 2);

      ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
      ctx.fillStyle = "rgb(50,50,50)";
      ctx.fillRect(0, 0, 1000, 1000);
      // eslint-disable-next-line no-unused-vars
      for (const [player_id, player] of Object.entries(env_status["player"])) {
        await draw_player(player);
      }
      for (const idx in env_status["bullet"]) {
        await draw_bullet(env_status["bullet"][idx]);
      }
    }

    function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function run() {
      draw();
      await sleep(1000 / FPS);
      window.requestAnimationFrame(run);
    }

    run();
  }
}


</script>

<style scoped>
#myCanvas {
  border: 20px solid lightgray;
  /*image-rendering: pixelated;*/
  height: 500px;
}

p {
  color: gray;
  text-align: left;
}

#response {
  color: gray;
  font-size: 10px;
  font-weight: bold;
  text-align: left;
  height: 440px;
  overflow-y: scroll;
  width: 316px;
  overflow-x: scroll;
}

#move_key {
  text-align: center;
  width: 20px;
  border-radius: 5px;
  border: 2px solid lightgray;
  margin-left: 5px;
  margin-top: 5px;
  margin-bottom: 0;
}

#notice, p {
  color: gray;
}
</style>