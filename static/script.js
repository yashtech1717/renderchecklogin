const searchInput = document.getElementById("searchInput");

if(searchInput){
    searchInput.addEventListener("keyup", function () {

        const filter = this.value.toLowerCase();
        const rows = document.querySelectorAll("#userTable tbody tr");

        rows.forEach(row => {

            const username =
                row.cells[1].textContent.toLowerCase();

            if(username.includes(filter)){
                row.style.display = "";
            }else{
                row.style.display = "none";
            }

        });

    });
}

document.querySelectorAll(".btn").forEach(btn => {

    btn.addEventListener("mousemove", function(e){

        const x =
            e.pageX - this.offsetLeft;

        const y =
            e.pageY - this.offsetTop;

        this.style.background =
        `radial-gradient(circle at ${x}px ${y}px,
        rgba(255,255,255,0.3),
        rgba(0,247,255,0.6),
        rgba(255,0,255,0.7))`;

    });

    btn.addEventListener("mouseleave", function(){

        this.style.background =
        "linear-gradient(90deg,#00f7ff,#ff00ff)";

    });

});