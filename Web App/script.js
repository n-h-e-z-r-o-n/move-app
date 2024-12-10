// -----------------------------Slide Show Function ------------------------------------------------------------
var element = document.getElementById("trending_container");

function start_slider(){
 jQuery(document).ready(function ($) {
         $(".slider-img").on("click", function () {
           if ($(this).hasClass("active")) {
             const redirectUrl = this.dataset.redirectUrl;
             //console.log(redirectUrl);
             window.location.href = "watch_page.html?id=" + redirectUrl + "&type=movie";
           } else {
             $(".slider-img").removeClass("active");
             $(this).addClass("active");
           }
         });
       });

  jQuery(document).ready(function ($) {
        let currentIndex = 0;
        const images = $(".slider-img");
        const imageCount = images.length;

        function showNextImage() {
            images.removeClass("active");
            currentIndex = (currentIndex + 1) % imageCount;
            images.eq(currentIndex).addClass("active");
        }

        // Automatically change the image every 3 seconds
        setInterval(showNextImage,1000);

        // Add click event to redirect when an active image is clicked

    });
  }
    // ------------------------------------------------------------------------------------------

    function AutoScroll_TRENDING() {
      const arrows = document.querySelectorAll(".arrow");
      const movieLists = document.querySelectorAll(".movie-list");

      arrows.forEach((arrow, i) => {
        const itemNumber = movieLists[i].querySelectorAll("img").length;
        let clickCounter = 0;

        const clickNext = () => {
          const ratio = Math.floor(window.innerWidth / 270);
          clickCounter++;
          const movieList = movieLists[i];
          const computedStyle = window.getComputedStyle(movieList);
          const transformValue = computedStyle.getPropertyValue("transform");
          const currentTranslateX = parseInt(transformValue.split(",")[4]) || 0;

          if (itemNumber - (4 + clickCounter) + (4 - ratio) >= 0) {
            movieList.style.transform = `translateX(${currentTranslateX - 300}px)`;
          } else {
            movieList.style.transform = "translateX(0)";
            clickCounter = 0;
          }
        };

        arrow.addEventListener("click", clickNext);
        setInterval(clickNext, 3000);   // Auto-click the next arrow after 3 seconds
      });
    }



//ppppppppppppppppppppppppppppp


function AutoScrollBothDirections() {
  const leftArrows = document.querySelectorAll(".left-arrow");
  const rightArrows = document.querySelectorAll(".right-arrow");
  const movieLists = document.querySelectorAll(".movie-list");

  movieLists.forEach((movieList, i) => {
    const itemNumber = movieList.querySelectorAll("img").length;
    let clickCounter = 0; // Track current scroll position
    const ratio = Math.floor(window.innerWidth / 270); // Adjust for visible items

    const scroll = (direction) => {
      const computedStyle = window.getComputedStyle(movieList);
      const transformValue = computedStyle.getPropertyValue("transform");
      const currentTranslateX = parseInt(transformValue.split(",")[4]) || 0;

      if (direction === "right") {
        if (itemNumber - (4 + clickCounter) + (4 - ratio) > 0) {
          movieList.style.transform = `translateX(${currentTranslateX - 300}px)`;
          clickCounter++;
        } else {
          movieList.style.transform = "translateX(0)";
          clickCounter = 0;
        }
      } else if (direction === "left") {
        if (clickCounter > 0) {
          movieList.style.transform = `translateX(${currentTranslateX + 300}px)`;
          clickCounter--;
        }
      }
    };

    rightArrows[i].addEventListener("click", () => scroll("right"));
    leftArrows[i].addEventListener("click", () => scroll("left"));
  });
}


setInterval(() => {
  document.querySelectorAll(".right-arrow").forEach((arrow) => {
    arrow.click(); // Trigger right-arrow click event
  });
}, 3000);

setInterval(() => {
  document.querySelectorAll(".left-arrow").forEach((arrow) => {
    arrow.click(); // Trigger left-arrow click event
  });
}, 6000); // Delayed to alternate with right scroll


//======================================= movie fetch --code block===================================================


const Movies_API_URL =   "https://api.themoviedb.org/3/discover/movie?&api_key=6bfaa39b0a3a25275c765dcaddc7dae7";
const TVs_API_URL =   "https://api.themoviedb.org/3/discover/tv?primary_release_year=2024&api_key=6bfaa39b0a3a25275c765dcaddc7dae7";
const Trending_API_URL =   "https://api.themoviedb.org/3/trending/all/day?primary_release_year=2024&api_key=af9b2e27c1a6bc3233af1832f4acc850";

const IMG_PATH = "https://image.tmdb.org/t/p/w1280";
const SEARCH_MOVIE_API = "https://api.themoviedb.org/3/search/movie?api_key=6bfaa39b0a3a25275c765dcaddc7dae7&query=";
const SEARCH_TV_API = "https://api.themoviedb.org/3/search/tv?api_key=6bfaa39b0a3a25275c765dcaddc7dae7&query=";

const Slider_div = document.getElementById("sliderUl");
const movie_div = document.getElementById("movieUl");
const series_div = document.getElementById("seriesUl");
const Trending_div = document.getElementById("TrendingUl");



const form = document.getElementById("searchForm");
const search = document.getElementById("search_input");


const  Latest_Movies_List_link =  "https://vidsrc.to/vapi/episode/latest/" ;
const  Latest_episode_List_link = "https://vidsrc.to/vapi/episode/latest";


const page_count = 1;
if (movie_div) {
    trendingShows(Trending_API_URL)

    //Slider_Movies(Movies_API_URL); // initial Movies
    //Slider_Movies(TVs_API_URL);

    Math.random() < 0.5 ? Slider_Movies(Movies_API_URL) : Slider_Movies(TVs_API_URL);

    Latest_Movies(null, page_count, 'add');
    Latest_episode(null, page_count);
  }

//SLIDER_ function --------------------------------------------------------------------------------

async function Slider_Movies(url) {
  const res = await fetch(url);
  const data = await res.json();
  console.log(data.results)
  Slider_Display(data.results);
}

function Slider_Display(movies) {
  Slider_div.innerHTML = "";
  let count = 0 ; // Math.floor(Math.random() * (11 - 0) + 0);

  let count_max = count + 19;
  let start = 0;
  console.log(count);
  movies.forEach((movie, index) => {
    if (count < count_max && index >= count){
          let  show_name;
          let updatedString;
          const { title, original_name, backdrop_path, first_air_date, poster_path, id, vote_average, overview, release_date } = movie;

          if (title === undefined){
          show_name = original_name;
          updatedString = first_air_date.substring(0, 4);
          }else{
          show_name= title;
          updatedString = release_date.substring(0, 4);
          }



          const movieItem = document.createElement("div");
          movieItem.classList.add("slider-img");
          movieItem.innerHTML = `
                <img src="${IMG_PATH + backdrop_path}" />
                <div class="details">
                  <h2 class="details_h2">${show_name}</h2>
                  <p class="details_p">&#9733; ${vote_average}</p>
                  <p class="details_p">${updatedString}</p>
                </div>
          `;
          movieItem.dataset.redirectUrl = `${id}`;
          Slider_div.appendChild(movieItem);
          start = movieItem;
          count++;
    }
  });
  start_slider();
  start.classList.add("active");

}


// get Movies and shows --------------------------------------------------------


async function Latest_Movies(event, page, type) {

  try{
    const choiceSelect = event.target;
    const choiceDivs = document.querySelectorAll('.show_title_section_movie button');
    choiceDivs.forEach(div => div.classList.remove('selected_glow'));
    choiceSelect.classList.add('selected_glow');
  } catch{console.log();}

  let count = 1;
  let data_json = [];

  while (count <= page) {
      let res = await fetch(`https://vidsrc.xyz/movies/latest/page-${page}.json`);
      let data = await res.json();
      data_json = data_json.concat(data['result']) ;
      count++;
      break;
    }

  let hold = [];
  for (let i = 0; i < data_json.length; i++) {

    let res2 = await fetch(`https://api.themoviedb.org/3/movie/${data_json[i]['tmdb_id']}&?api_key=6bfaa39b0a3a25275c765dcaddc7dae7`);
    let data2 = await res2.json();
    hold.push({poster_path:data2['poster_path'], release_date:data2['release_date'], vote_average:data2['vote_average'], title:data2['title'], id:data2['id'], runtime:data2['runtime']});
  }
  showMovies(hold);
}





async function Latest_episode(event, page) {
  try{
    const choiceSelect = event.target;
    const choiceDivs = document.querySelectorAll('.show_title_section_show button');
    choiceDivs.forEach(div => div.classList.remove('selected_glow'));
    choiceSelect.classList.add('selected_glow');
  } catch{console.log();}

  let count = 1;

  let data_json = [];
  let id_prev = 0;

  while (count <= page) {
      let res = await fetch(`https://vidsrc.xyz/episodes/latest/page-${page}.json`);

      let data = await res.json();
      if(Array.isArray(data['result'])){
        data_json = data_json.concat(data['result']) ;
        count++;
      }else{
        itemValues = Object.values(data.result);
        data_json = data_json.concat(itemValues) ;
        count++;
      }
      break;
    }
  let hold = [];
  for (let i = 0; i < data_json.length; i++) {
      try{
          let res2 = await fetch(`https://api.themoviedb.org/3/tv/${data_json[i]['tmdb_id']}&?api_key=6bfaa39b0a3a25275c765dcaddc7dae7`);
          let data2 = await res2.json();

          let  seasons_episode = '';




          if(`${data2['poster_path']}` !== `undefined`){
            if (id_prev !==data2['id']){

                try{
                   seasons_episode =   `SS ${data2['number_of_seasons']} / ESP ${data2['last_episode_to_air']['episode_number']}`;
                }catch (error) {
                  seasons_episode =  `SS ${data2['number_of_seasons']} / ESP ${data2['number_of_episodes']}`;
                }


                hold.push({poster_path:data2['poster_path'], first_air_date:data2['first_air_date'], vote_average:data2['vote_average'], original_name:data2['original_name'], id:data2['id'], S_info: seasons_episode});
                id_prev = data2['id'];

            }
          }
        }finally{continue;}
  }
  showTV(hold);
}

// SHOW MOVIES  SECTION --------------------------------------------------------


function showMovies(movies) {
  //movie_div.innerHTML = "";
  movies.forEach((movie) => {
    const { title, poster_path, id, vote_average, overview, release_date, runtime } = movie;
    const movieItem = document.createElement("div");
    movieItem.classList.add("box");
    let updatedString = release_date.substring(0, 4);
    movieItem.innerHTML = `
        <!-- box-1  -->

             <div class="box-img">
                <img class="img-on" src="${IMG_PATH + poster_path}" alt="">
                <div class="box-img-button">
                     <div class="button_style">&#9654;</div>
                     <div class="button_style" style="background-color: black;">+</div>
                </div>
            </div>
            <div class="box_title">${title}</div>
            <div class="container_span">
               <div style="display:flex;">
                    <div  class="badge-type"> mv </div>
                    <div class="badge-type_year">${updatedString} </div>
               </div>
               <div class="badge-type_text"> ${runtime} min</div>
               <div  class="badge-type_rating"> &starf;  ${vote_average} </div>
            </div>

    `;

    // Add event listener to open another page when clicked
    //movieItem.addEventListener("click", () => {
    //     window.location.href = "watch_page.html?id=" + id + "&type=movie";
    //   });


    const boxImg = movieItem.querySelector(".box-img");
    boxImg.addEventListener("click", () => {
      window.location.href = "watch_page.html?id=" + id + "&type=movie";
    });

    movie_div.appendChild(movieItem);
  });
}


// SHOW TV SECTION -----------------------------------------------------------------------

function showTV(movies) {
  //series_div.innerHTML = "";
  movies.forEach((movie) => {
    const {id, original_name, poster_path, vote_average, overview, first_air_date, S_info } = movie;
    let updatedString = first_air_date.substring(0, 4);
    const movieItem = document.createElement("div");
    movieItem.classList.add("box");
    movieItem.innerHTML = `
        <!-- box-1  -->

            <div class="box-img">
                <img class="img-on" src="${IMG_PATH + poster_path}" alt="">
                <div class="box-img-button">
                     <div class="button_style">&#9654;</div>
                     <div class="button_style" style="background-color: black;">+</div>
                </div>
            </div>
            <div class="box_title">${original_name}</div>
            <div class="container_span">
               <div style="display:flex;">
                    <div  class="badge-type"> tv </div>
                    <div class="badge-type_year"> ${updatedString} </div>
               </div>
               <div class="badge-type_text"> ${S_info} </div>
               <div  class="badge-type_rating"> &starf;  ${vote_average} </div>
            </div>

    `;

    // Add event listener to open another page when clicked
    //movieItem.addEventListener("click", () => {
    //     window.location.href = "watch_page.html?id=" + id + "&type=tv";
    //   });

    const boxImg = movieItem.querySelector(".box-img");
    boxImg.addEventListener("click", () => {
      window.location.href = "watch_page.html?id=" + id + "&type=tv";
    });

    series_div.appendChild(movieItem); // Append the `movieItem` to the container
  });
}

// SHOW TRENDING SECTION --------------------------------------------------------
async function trendingShows(url) {
  const res = await fetch(url);
  const data = await res.json();
  console.log('trending ', data.results);
  showsTrending(data.results);
}



function showsTrending(movies) {
  Trending_div.innerHTML = "";
  movies.forEach((movie) => {
    const { id, media_type, original_title, original_name, poster_path, vote_average, overview, first_air_date } = movie;
    let title;

    if (original_title=== undefined) {
       title = original_name;

    } else {
       title = original_title;
    }
    const movieItem = document.createElement("div");
    movieItem.classList.add("movie-list-item");
    movieItem.innerHTML = `

                  <img class="movie-list-item-img" src="${IMG_PATH + poster_path}" alt="">
                  <button class="movie-list-item-button" onclick="redirect_function(${id}, '${media_type}')">Watch</button>
                  <div class="movie-list-item-title"> ${title}</div>
    `;

    Trending_div.appendChild(movieItem);
  });
   AutoScroll_TRENDING();
}

function redirect_function(id, media_type) {
  console.log("watch clicker", id, media_type);
  window.location.href = "watch_page.html?id=" + id + `&type=${media_type}`;
}


//========================================================================================
//========================================================================================

function Search_Results_SHOW(movies) {
  console.log(movies);
  search_R_div.innerHTML = "";
  movies.forEach((movie) => {
    const { original_title, original_name, poster_path, vote_average, overview, first_air_date } = movie;
    let title;

    if (original_title=== undefined) {
       title = original_name;

    } else {
       title = original_title;
    }
    const movieItem = document.createElement("div");
    movieItem.classList.add("movie-list-item");
    movieItem.innerHTML = `

              <!-- box-1  -->

                  <div class="box-img">
                      <img src="${IMG_PATH + poster_path}"  alt="">
                  </div>
                  <h3>${title}</h3>
                  <div class="container_span">
                     <div style="color: gray;">${first_air_date}</div>
                     <div style="color: gray;"> &starf; &starf; &#9734;   ${vote_average}</div>
                  </div>


    `;
    search_R_div.appendChild(movieItem);
  });
}
// FOR SEARCH SUBMIT


form.addEventListener("submit", (e) => {
  e.preventDefault();
  const searchTerm = search.value;
  if (searchTerm && searchTerm !== "") {

    search.value = "";
    window.location.href = "S_Results.html?query=" + searchTerm; // Replace with the URL of the page you want to open
  } else {

  }
});

//

//============================================================================== SHOW MORE FUNCTIONS
let movie_currentPage = 1;

async function more_movie(){

  const button = document.getElementById("moreMovieButton");
  const state = button.getAttribute('data-state');

  if (state ==='show-more'){
            button.textContent = "Loading...";
            button.setAttribute('data-state', 'loading');

            movie_currentPage = movie_currentPage + 1;

            let data_json = [];

            let res = await fetch(`https://vidsrc.xyz/movies/latest/page-${movie_currentPage}.json`);
            let data = await res.json();
            data_json = data_json.concat(data['result']) ;

            let hold = [];
            for (let i = 0; i < data_json.length; i++) {

            let res2 = await fetch(`https://api.themoviedb.org/3/movie/${data_json[i]['tmdb_id']}&?api_key=6bfaa39b0a3a25275c765dcaddc7dae7`);
            let data2 = await res2.json();
            hold.push({poster_path:data2['poster_path'], release_date:data2['release_date'], vote_average:data2['vote_average'], title:data2['title'], id:data2['id']});
            }
            button.innerHTML = "Show More &#x21b4;";
            button.setAttribute('data-state', 'show-more');
            showMovies(hold)
    }
}



let series_currentPage = 1;
async function more_series(){

  const button = document.getElementById("moretvButton");
  const state = button.getAttribute('data-state');


  if (state ==='show-more'){
            button.textContent = "Loading...";
            button.setAttribute('data-state', 'loading');

            series_currentPage = series_currentPage + 1;

            let data_json = [];
            let id_prev = 0;

            let res = await fetch(`https://vidsrc.xyz/episodes/latest/page-${series_currentPage}.json`);
            let data = await res.json();
            if(Array.isArray(data['result'])){
                 data_json = data_json.concat(data['result']) ;
            }else{
                itemValues = Object.values(data.result);
                data_json = data_json.concat(itemValues) ;
            }

            let hold = [];
            for (let i = 0; i < data_json.length; i++) {
              try{
                  let res2 = await fetch(`https://api.themoviedb.org/3/tv/${data_json[i]['tmdb_id']}&?api_key=6bfaa39b0a3a25275c765dcaddc7dae7`);
                  let data2 = await res2.json();
                  if(`${data2['poster_path']}` !== `undefined`){
                    if (id_prev !==data2['id']){
                      hold.push({poster_path:data2['poster_path'], first_air_date:data2['first_air_date'], vote_average:data2['vote_average'], original_name:data2['original_name'], id:data2['id']});
                      id_prev = data2['id'];
                    }
                  }
                }finally{continue;}
            }
            button.innerHTML = "Show More &#x21b4;";
            button.setAttribute('data-state', 'show-more');
            showTV(hold);
}
}


// =============================================================================


$(document).ready(function(){
            $('.toggle').click(function(){
                $('.menu').toggleClass('active');
            });
        });
