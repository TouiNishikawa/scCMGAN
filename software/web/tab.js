const aside = document.getElementsByTagName("aside")[0];
const aside_tablists = aside.getElementsByTagName("g");
const mains = mainwrap.getElementsByTagName("main");

for(const aside_tablist of aside_tablists){
    aside_tablist.addEventListener("click", function(e){
        if(this.classList.contains("enable")){
            for(let i=0; i<aside_tablists.length; i++){
                if(aside_tablists[i].classList.contains("active") && this != aside_tablists[i]){
                    aside_tablists[i].classList.remove("active");
                    mains[i].style.display="none";
                }
                if((!aside_tablists[i].classList.contains("active")) && this == aside_tablists[i]){
                    this.classList.add("active");
                    mains[i].style.display="flex";
                }
            }
        }
    });
}

