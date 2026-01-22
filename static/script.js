function enviarClique(nomeBotao) {
    fetch('/clique', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ botao: nomeBotao })
    })
    .then(res => res.json())
    .then(data => {
        const div = document.getElementById('info-clique');
        div.innerHTML = `
            <p><strong>Botão:</strong> ${nomeBotao}</p>
            <p><strong>Sequencial do dia:</strong> ${data.sequencial}</p>
            <p><strong>Data:</strong> ${data.data}</p>
            <p><strong>Hora:</strong> ${data.hora}</p>
        `;
    });
}