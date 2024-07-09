// Function to compare a given date with today
function compareWithToday(dateString) {
    // Create Date objects for the given date and today's date
    const givenDate = new Date(dateString);
    const today = new Date();

    // Set time to 00:00:00 for both dates to only compare the date part
    givenDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    // Compare the dates
    if (givenDate > today) {
        return false;
    } else {
        return true;
    }
}

//------------------------------------------------------------------------------

const watch_info = document.getElementById("watch_info");
const watch_Frame = document.getElementById("watch_Frame");

const IMG_PATH = "https://image.tmdb.org/t/p/w1280";
let episodes = {};
let show_id = 1;

async function SHOW_INFOs(id, type) {
  const res = await fetch(`https://api.themoviedb.org/3/${type}/${id}&?api_key=6bfaa39b0a3a25275c765dcaddc7dae7`);
  const data = await res.json();
  Search_Results_SHOW(id, type, data);

}

function Search_Results_SHOW(imdb, type, info_data) {
  var element = document.getElementById("back_img");
  let PG = 18;
  console.log(info_data);
  if (type == 'movie'){
    console.log(type);

    console.log(info_data);
  }else{  }


  element.style.background = `linear-gradient(to bottom, rgba(0, 0, 0, 0), var(--global-color-bg)), url("${IMG_PATH}${info_data['backdrop_path']}")`;

  if(info_data['adult'] ===  false){
    PG = 13;
  }
  let genres = ""
   for (let i = 0; i < info_data['genres'].length; i++) {
     genres = genres.concat(' ', info_data['genres'][i].name, ', ');
   }

   let production_companies = ""
    for (let i = 0; i < info_data['production_companies'].length; i++) {
      production_companies = production_companies.concat(' ', info_data['production_companies'][i].name, ', ');
    }

  if (type==="movie"){
               let title = info_data['title'];
               if (title === "undefined"){
                 title = info_data['original_name'];
               }
                watch_info.innerHTML = `
                      <img class="watch_image" src="${IMG_PATH+info_data['poster_path']}">
                      <div class="watch_details">
                          <h3 class="watch_title">${title}</h3>
                          <ul >
                            <li class="movie_gen__details">PG-${PG}  /</li>
                            <li class="movie_gen__details"> ${info_data['runtime']} min  /</li>
                            <li class="movie_gen__details">${info_data['original_language']}</li>
                          </ul>

                          <p class="watch_review">${info_data['overview']}</p>
                          <p class="watch_review" style="color:gray;">&starf; &starf; &#9734;   ${info_data['vote_average']}</p>
                          <p class="watch_review" style="color:gray;">Type: Movie</p>

                          <div>
                            <div class="watch_review">Genres &nbsp; </div>
                            <div class="watch_review" style="color:gray; padding-left: 20px;">${genres} </div>
                          </div>
                          <div >
                                <p class="watch_review">Production &nbsp;</p>
                                <p class="watch_review" style="color:gray; padding-left: 20px;">${production_companies}</p>
                          </div>
                          <div >
                                <p class="watch_review">release_date &nbsp;</p>
                                <p class="watch_review" style="color:gray; padding-left: 20px;">${info_data['release_date']}</p>

                          </div>


                      </div>
                `;

                watch_Frame.innerHTML = `<iframe  class="iframe_watch"  id="watch-frame" onerror="iframeLoadError()" src="https://vidsrc.to/embed/${type}/${imdb}"  frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>`;
                //watch_Frame.innerHTML = `<iframe  class="iframe_watch"  id="watch-frame" src="https://multiembed.mov/?video_id=${imdb}&tmdb=1"  frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>`;


}else{

  let title = info_data['title'];
  if (`${title}` === `undefined`){
    title = info_data['original_name'];
  }


  watch_info.innerHTML = `
        <img class="watch_image" src="${IMG_PATH+info_data['poster_path']}">
        <div class="watch_details">
            <h3 class="watch_title">${title}</h3>
            <ul >
              <li class="movie_gen__details">PG-${PG}  /</li>
              <li class="movie_gen__details"> ${info_data['episode_run_time']} min  /</li>
              <li class="movie_gen__details">${info_data['original_language']}</li>
            </ul>

            <p class="watch_review">${info_data['overview']}</p>
            <p class="watch_review" style="color:gray;">&starf; &starf; &#9734;   ${info_data['vote_average']}</p>
            <p class="watch_review" style="color:gray;">Type: series</p>
            <div>
              <div class="watch_review">Genres &nbsp; </div>
              <div class="watch_review" style="color:gray; padding-left: 20px;">${genres} </div>
            </div>

            <div >
                  <p class="watch_review">Production &nbsp;</p>
                  <p class="watch_review" style="color:gray; padding-left: 20px;">${production_companies}</p>
            </div>
            <div >
                  <p class="watch_review">First-air date &nbsp;</p>
                  <p class="watch_review" style="color:gray; padding-left: 20px;">${info_data['first_air_date']}</p>
            </div>
            <div >
                  <p class="watch_review">Last-air date &nbsp;</p>
                  <p class="watch_review" style="color:gray; padding-left: 20px;">${info_data['last_air_date']}</p>
            </div>


        </div>
  `;

  watch_Frame.innerHTML = `<iframe  class="iframe_watch" id="watch-frame" onerror="iframeLoadError()" src="https://vidsrc.to/embed/${type}/${imdb}"  frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>`;
  //https://vidsrc.to/embed/${type}/${imdb}/{season}/{episode}


  let se = info_data['seasons'];
  se = se.filter(se => se.air_date !== null);
  let con = ``;

  const season_selector =  document.getElementById("season-selector");


  let sub = 1;

  for (let i = 0; i < se.length; i++) {
        if(se[i]['name'] === "Specials"){
            sub = sub - 1;
            continue;
         }

        let j = i+sub;

        if (i < (se.length-1)){
              con = con +  `<div data-season="season1" onclick="displayEpisodes(event, ${j})">${se[i]['name']}</div> `;
              let episodeCount = se[i]['episode_count'];
              episodes[j] = []; // Initialize the array
              // Create an array from 1 to episodeCount
              for (let k = 1; k <= episodeCount; k++) {  episodes[j].push(k); }
        } else {

                con = con +  `<div data-season="season1" onclick="displayEpisodes(event, ${j})">${se[i]['name']}</div> `;
                let episodeCount = se[i]['episode_count'];
                try {
                    let stat = compareWithToday(info_data['next_episode_to_air']['air_date']);
                    let last_ep = info_data['next_episode_to_air']['episode_number'];
                    if (last_ep < episodeCount){
                            if(!stat){  episodeCount = last_ep-1; }
                            else{  episodeCount = last_ep;      }
                    }
                } finally {
                    episodes[j] = []; // Initialize the array
                    for (let k = 1; k <= episodeCount; k++) {  episodes[j].push(k); }
                    break;
                }
            }
  }
  season_selector.innerHTML = ` ${con}`;
  console.log('episodes', episodes);
//season_selector.appendChild(movieItem);
}
}
// FOR SEARCH SUBMIT-----------------------------------------------------------------------------------------------------------
const form = document.getElementById("searchForm");
const search = document.getElementById("search_input");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const searchTerm = search.value;
  if (searchTerm && searchTerm !== "") {

    search.value = "";
    window.location.href = "S_Results.html?query=" + searchTerm; // Replace with the URL of the page you want to open
  } else {

  }
});

// ---------------------------------------------------------------------------------------------------------------
const Movies_API_URL =   "https://api.themoviedb.org/3/discover/movie?&api_key=6bfaa39b0a3a25275c765dcaddc7dae7";
const TVs_API_URL =   "https://api.themoviedb.org/3/discover/tv?&api_key=6bfaa39b0a3a25275c765dcaddc7dae7";
const recomed_R_div =  document.getElementById("recomed_R_div");


function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}


async function Suggestion_Show() {
  let randomInt = getRandomInt(5, 495); // Generates a random integer between 5 and 15 (inclusive)
  const res1 = await fetch(Movies_API_URL+"&page="+randomInt);
  const data1 = await res1.json();

  const res2 = await fetch(TVs_API_URL+"&page="+randomInt);
  const data2 = await res2.json();

  const combinedData =data1.results.concat(data2.results);
  Suggestion_Search(combinedData) ;
}

function Suggestion_Search(movies) {
  recomed_R_div.innerHTML = "";
  movies.forEach((movie) => {
    const { original_title, original_name, poster_path, id, vote_average, overview, release_date, first_air_date } = movie;
    let title;
    let type;
    if (original_title=== undefined) {
       title = original_name;
       date = first_air_date;
        type = "tv";

    } else {
       title = original_title;
       date = release_date
        type = "movie";
    }

    const movieItem = document.createElement("div");
    movieItem.classList.add("box");
    movieItem.innerHTML = `

              <!-- box-1  -->
              <div class="imgBx">
                <img src="${IMG_PATH + poster_path}">
              </div>
              <div class="content">
                <div>
                  <h2>${title}</h2>
                  <p>${overview}</p>
                  <p>&starf; &starf; ${vote_average}</p>
                </div>
              </div>

    `;
    // Add event listener to open another page when clicked
    movieItem.addEventListener("click", () => {
         window.location.href = "watch_page.html?id=" + id + "&type="+type;
       });
    recomed_R_div.appendChild(movieItem);
  });
}

//---------------------------------------------------------------------------------------------------------------------


// Function to get URL parameters
 function getQueryParams() {
     const params = {};
     const queryString = window.location.search.substring(1);
     const regex = /([^&=]+)=([^&]*)/g;
     let m;
     while (m = regex.exec(queryString)) {
         params[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
     }
     return params;
 }






 // Extract the search term from URL parameters
 const params = getQueryParams();
 console.log(params);

 if (params) {
   const watch_id = params['id'];
   const watch_type = params['type'];

  //Search_Results_SHOW(watch_id, watch_type);
   show_id = watch_id;
   SHOW_INFOs(watch_id, watch_type);
   Suggestion_Show();


 } else { }



 function displayEpisodes(event, season_no) {
           console.log(`Season clicked: ${season_no}`); // Log the season ID

           const seasonSelect = event.target;
           const season = seasonSelect.getAttribute("data-season");
           // Remove 'selected' class from all divs
           const seasonDivs = document.querySelectorAll('.season-selector div');
           console.log("seasonDivs", seasonDivs);

           seasonDivs.forEach(div => div.classList.remove('selected'));
           seasonSelect.classList.add('selected');            // Add 'selected' class to the clicked div

           const episodeList = document.getElementById("episode-list");
           episodeList.innerHTML = "";// Clear current episodes
           const selectedEpisodes = episodes[season_no];            // Get episodes for the selected season
           // Display episodes
           selectedEpisodes.forEach(episode => {
             const li = document.createElement("div");
             li.classList.add("episodes_each");


             li.textContent = `Episode ${episode}`;
             li.addEventListener("click", (event) => {
               const episodeSelect = event.target;
               const episodeDivs = document.querySelectorAll('.episodes div');
               episodeDivs.forEach(div => div.classList.remove('selected'));
               console.log("Episod", episodeDivs);

               episodeSelect.classList.add('selected');

               const iframe = document.getElementById("watch-frame");
               const newSrc = `https://vidsrc.to/embed/tv/${show_id}/${season_no}/${episode}`;
               iframe.src = newSrc;

             });
             episodeList.appendChild(li);
           });
       }
