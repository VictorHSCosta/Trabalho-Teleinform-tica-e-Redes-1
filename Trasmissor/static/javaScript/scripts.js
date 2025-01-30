function verificarIP() {
  const ip = document.getElementById("ipInput").value;
  const status = document.getElementById("status");

  fetch("/verificar_ip", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ip: ip }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.sucesso) {
        setTimeout(() => {
          window.location.href = "/home";
        }, 2000);
      } else {
        status.innerHTML = "❌ " + data.erro;
      }
    })
    .catch((error) => {
      status.innerHTML = "❌ Erro na requisição!";
    });
}
