function DoSubmit(value) {
    document.myform.game_id.value = value;
}


var objective = 0;
console.log(destination.length);
for (let i = destination.length + 1; i < 6; i++) {
    id = "distance" + i;
    console.log(id);
    let element = document.getElementById(id);
    element.style.display = "none";
    //element.style.display = "block";
}

function initMap() {
    const uluru = home; //Unde incepe user-ul
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: uluru,
        disableDefaultUI: true,
    });
    const panorama = new google.maps.StreetViewPanorama(
        document.getElementById("map"),
        {
            linksControl: false,
            panControl: false,
            enableCloseButton: false,
            addressControl: false,
            addressControlOptions: false,

            position: uluru,
            pov: {
                heading: 34,
                pitch: 0,
            },
        }
    );

    panorama.addListener("position_changed", () => { //La fiecare miscare a user-ului
        clearTimeout(timeout);
        timeout = setTimeout("showDiv1()", 10000);
        document.getElementById("popup").style.visibility = "hidden";

        for (let i = 1; i <= destination.length; i++) {
            var current = destination[i - 1];
            var distance = google.maps.geometry.spherical.computeDistanceBetween(current, panorama.getPosition()) //distanta fata de destinatie
            id = "at" + i;
            id3 = "distance" + i;
            console.log(id);
            // document.getElementById(id2).innerHTML = names[i-1];
            // document.getElementById(id).innerHTML = "Not visited: " + names[i-1] + ", distance: " + Math.trunc(distance);

            if (document.getElementById(id).innerHTML != "Visited: " + names[i - 1]) {
                document.getElementById(id).innerHTML = "Not visited: " + names[i - 1] + ", distance: " + Math.trunc(distance) + " meters!";
            }
            if (distance < 20) {
                if (document.getElementById(id).innerHTML != "Visited: " + names[i - 1]) {
                    document.getElementById("name of destination1").innerHTML = "You have reached: ";
                    document.getElementById("name_of_destination2").innerHTML = names[i - 1];
                    document.getElementById("descriere").innerHTML = descrieri[i - 1];

                    const trivias = document.querySelectorAll('.trivia');
                    lista = document.getElementById("lista-dreapta")
                    trivias.forEach(triviaa => {
                        triviaa.remove();
                    });


                    for (var j = 0; j < trivia[i - 1].length; j++) {
                        const el = document.createElement('li');
                        el.classList.add('list-group-item', 'happy', 'trivia');
                        el.textContent = trivia[i - 1][j];
                        lista.appendChild(el);
                        console.log(trivia[i - 1][j]);
                    }

                    objective++;
                }
                document.getElementById(id3).style.backgroundColor = "#35b39a";
                document.getElementById(id).innerHTML = "Visited: " + names[i - 1];
            }
            //var element = document.getElementById(id).innerHTML =  "";
            //element.style.display = "block";
        }

        if (objective == destination.length) {
            //Done! What now?
            console.log("Game is over!");
            document.getElementById("endTrip").style.display = "inline"
        } else {


        }

    });

    map.setStreetView(panorama);
}
