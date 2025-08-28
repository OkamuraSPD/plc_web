
    document.querySelectorAll(".toggle").forEach(toggle => {
      toggle.addEventListener("change", () => {
        let id = toggle.dataset.id;
        let value = toggle.checked ? 1 : 0;
        console.log({ id: id, value: value });
        fetch("/toggle", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ id: id, value: value })
          
        })
        .then(res => res.json())
        .then(data => console.log("Server odpověděl:", data));
      });
    });
  