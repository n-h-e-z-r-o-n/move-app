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

  const combinedData =data1.results.concat(data2.results);
  Search_Results_SHOW(combinedData) ;
}

function Search_Results_SHOW(movies) {
  console.log(movies);
  search_R_div.innerHTML = "";
  movies.forEach((movie) => {
    const { original_title, original_name, poster_path, vote_average, overview, release_date, first_air_date } = movie;
    let title;

    if (original_title=== undefined) {
       title = original_name;
       date = first_air_date

    } else {
       title = original_title;
       date = release_date
    }

    const movieItem = document.createElement("div");
    movieItem.classList.add("box");
    movieItem.innerHTML = `

              <!-- box-1  -->



                  <div class="box-img">
                      <img src="${IMG_PATH + poster_path}"  alt="">
                  </div>
                  <h3>${title}</h3>
                  <div class="container_span">
                     <div style="color: gray;">${date}</div>
                     <div style="color: gray;"> ${" \t\t\t ★"} ${vote_average}</div>
                  </div>


    `;
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






 document.addEventListener('DOMContentLoaded', () => {
   const movieContainers = document.querySelectorAll('.box');

   movieContainers.forEach(container => {
     container.addEventListener('click', () => {
       // Add your desired action here
       console.log('Container clicked:', container);
       // For example, you could redirect to a movie detail page
       // window.location.href = 'path/to/detail/page';
     });
   });
 });
