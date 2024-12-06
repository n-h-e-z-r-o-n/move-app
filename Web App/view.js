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

 const params = getQueryParams();  // Extract the search term from URL parameters

 console.log(params)

 // FOR SEARCH SUBMIT -----------------------------------------------------------------
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
//------------------------------------------------------------------------------
const IMG_PATH = "https://image.tmdb.org/t/p/w1280";

const more_div = document.getElementById("moreUl");


async function Latest_shows(page) {
  let res = await fetch(`https://vidsrc.xyz/episodes/latest/page-${page}.json`);
  let data = await res.json();
  let hold = [];
  let data_json = [];
  console.log(params)
  if (params['query'] === 'show'){
   data_json  = data['result'];
   console.log("params show")
  }else{
   data_json  = data['result']['items'];
    console.log("params movie")
  }

  if(Array.isArray(data_json)){
  }else{
      itemValues = Object.values(data.result.items);
      data_json = itemValues;
  }

  let id_prev = 0;
  for (let i = 0; i < 15; i++) {
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

                hold.push({poster_path:data2['poster_path'], first_air_date:data2['first_air_date'], vote_average:data2['vote_average'], overview:data2['overview'], original_name:data2['original_name'], id:data2['id'], S_info: seasons_episode});
                id_prev = data2['id'];
                }
            }
          }finally{continue;}
  }
  console.log("show f: ", hold);
  Suggestion_Search(hold);
}


async function Latest_Movies(page) {
  let count = 1;
  let data_json = [];
  let res = await fetch(`https://vidsrc.xyz/movies/latest/page-${page}.json`);
  let data = await res.json();
  data_json = data_json.concat(data['result']) ;
  let data2;
  let hold = [];


  for (let i = 0; i < data_json.length; i++) {
    let res2 = await fetch(`https://api.themoviedb.org/3/movie/${data_json[i]['tmdb_id']}&?api_key=6bfaa39b0a3a25275c765dcaddc7dae7`);
    data2 = await res2.json();

    hold.push({poster_path:data2['poster_path'], release_date:data2['release_date'], vote_average:data2['vote_average'], original_title:data2['title'], original_name:data2['original_name'],  id:data2['id'], runtime:data2['runtime']});

  }
  Suggestion_Search(hold);
}


function Suggestion_Search(movies) {
  more_div.innerHTML = "";
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
    more_div.appendChild(movieItem);
  });
}

//==================================================================================
const items = Array.from({length: 500}, (_, i) => `Item ${i + 1}`);
const itemsPerPage = 5;
const maxVisiblePages = 5;
let currentPage = 1;

function renderPagination() {
  const pagination = document.getElementById('pagination');
  pagination.innerHTML = '';
  const totalPages = Math.ceil(items.length / itemsPerPage);
  const half = Math.floor(maxVisiblePages / 2);

  let startPage = currentPage - half;
  let endPage = currentPage + half;

  if (startPage < 1) {
    startPage = 1;
    endPage = Math.min(totalPages, maxVisiblePages);
  }

  if (endPage > totalPages) {
    endPage = totalPages;
    startPage = Math.max(1, totalPages - maxVisiblePages + 1);
  }

  const createButton = (text, page, isActive = false, isDisabled = false) => {
    const button = document.createElement('button');
    button.textContent = text;
    button.className = isActive ? 'active' : '';
    button.disabled = isDisabled;
    if (!isDisabled) {
      button.addEventListener('click', () => goToPage(page));
    }
    pagination.appendChild(button);
  };

  createButton('First', 1, false, currentPage === 1);
  createButton('Prev', currentPage - 1, false, currentPage === 1);

  for (let i = startPage; i <= endPage; i++) {
    createButton(i, i, i === currentPage);
  }

  createButton('Next', currentPage + 1, false, currentPage === totalPages);
  createButton('Last', totalPages, false, currentPage === totalPages);
}

function goToPage(page) {
  currentPage = page;
  if (params['query'] === 'show'){  Latest_shows(currentPage);
  } else{ Latest_Movies(currentPage); }
  renderPagination();
}
// =============================================================================
if (params['query'] === 'show'){
  console.log("DISP show");
  Latest_shows(1);
  renderPagination();// Initial render
}
else{
  console.log("DISP movies");
  Latest_Movies(1);
  renderPagination();// Initial render
}
