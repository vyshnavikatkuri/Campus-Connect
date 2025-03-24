let now = new Date();
let hours = now.getHours();
let minutes = now.getMinutes();
let seconds = now.getSeconds();

console.log(`Current Time: ${hours}:${minutes}:${seconds}`);

const myTimeout = setTimeout(myGreeting, 7000);

    function myGreeting() {
      window.location.replace("http://127.0.0.1:8000//userfinal");
    }