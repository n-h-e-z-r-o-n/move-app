// FOR SEARCH SUBMIT
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


const IMG_PATH = "https://image.tmdb.org/t/p/w1280";
const SEARCH_MOVIE_API = "https://api.themoviedb.org/3/search/movie?api_key=6bfaa39b0a3a25275c765dcaddc7dae7&query=";
const SEARCH_TV_API = "https://api.themoviedb.org/3/search/tv?api_key=6bfaa39b0a3a25275c765dcaddc7dae7&query=";

const search_R_div = document.getElementById("Search_Results");


async function SearchShows(url, url2) {
  const res1 = await fetch(url);
  const data1 = await res1.json();

  const res2 = await fetch(url2);
  const data2 = await res2.json();
  //console.log("show ", data1['results']);
  console.log("mvovie ", data2['results']);
  const combinedData =data1.results.concat(data2.results);
  Search_Results_SHOW(combinedData) ;
}

function Search_Results_SHOW(movies) {
  //console.log(movies);
  search_R_div.innerHTML = "";
  movies.forEach((movie) => {
    const { original_title, original_name, poster_path, id, vote_average, overview, release_date, first_air_date , runtime, S_info} = movie;
    //console.log(movie);
    let title;
    let type;
    let Info;

    if (original_title === undefined) {
       title = original_name;
       date = first_air_date.substring(0, 4);
       type = "tv";
       info = S_info;

    } else {
        title = original_title;
        date = release_date.substring(0, 4);
        type = "mv";
        info = `${runtime} min` ;
    }

    const movieItem = document.createElement("div");
    movieItem.classList.add("box");
    movieItem.innerHTML = `
             <div class="box-img">
                <img class="img-on" src="${IMG_PATH + poster_path}" alt="">
                <div class="box-img-button">
                     <div class="button_style">&#9654;</div>
                     <div class="button_style">+</div>
                </div>
            </div>
            <div class="box_title">${title}</div>
            <div class="container_span">
               <div style="display:flex;">
                    <div  class="badge-type"> ${type} </div>
                    <div class="badge-type_year"> ${date} </div>
               </div>
               <div class="badge-type_text"> ${info}</div>
               <div  class="badge-type_rating"> &starf;  ${vote_average} </div>
            </div>

    `;
    // Add event listener to open another page when clicked
    movieItem.addEventListener("click", () => {
         window.location.href = "watch_page.html?id=" + id + "&type="+type;
       });
    search_R_div.appendChild(movieItem);
  });
}

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
 const searchTerm = params['query'];

 if (searchTerm) {
   document.getElementById('result_text').innerText = `SEARCH RESULTS      :  ${searchTerm}`;
   SearchShows(SEARCH_MOVIE_API + searchTerm, SEARCH_TV_API+searchTerm);    // code to fetch and display search results here
 } else { }
