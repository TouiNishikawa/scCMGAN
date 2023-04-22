let database=null;

async function onDatabaseSelected(){
    let path = await eel.selectFile("csv file\0*.csv\0\0", false)();
    if(path.length!=0){
        database = await eel.setDatabase(path)();
        document.getElementById("visualize").classList.add("enable");
        document.getElementById("dectgan").classList.add("enable");
        
        new Chart(document.getElementById("cellnumchart").getContext("2d"), {
            type: 'bar',
            data: {
                labels: database[0],
                datasets: [{
                    label: '# of Cells',
                    data: database[1],
                    borderWidth: 1
                }]
            },
            options:{
                responsive:false,
                indexAxis: 'y',
            }
        });

        dectgan_celltype = document.getElementById("dectgan_celltype");
        let text = "";
        for(const celltype of database[0]){
            text += "<option value=\"" + celltype + "\">" + celltype + "</option>";
        }
        dectgan_celltype.innerHTML = text;
    }
}

let isRunning = false;
function onStartVisualize(){
    if(!isRunning){
        isRunning = true;
        document.getElementById("processrunning").style.display="block";
        setTimeout(onStartVisualize_sub, 10);
    }
}
async function onStartVisualize_sub(){
    const umap = await eel.runUmap()();
    const datasets = [];
    const cellnumber = database[2].length;
    for(const celltype of database[0]){
        let data = [];
        for(let i=0;i<cellnumber;i++){
            if(database[2][i] == celltype){
                data.push({x:umap[i][0],y:umap[i][1]});
            }
        }
        datasets.push({label:celltype,data:data});
    }
    const ctx = document.getElementById("scatter_1").getContext("2d");
    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: datasets,
        },
        options:{
            responsive:false,
        }
    });
    isRunning = false;
    document.getElementById("processrunning").style.display="none";
}

function onStartGAN(){
    if(!isRunning){
        isRunning = true;
        document.getElementById("processrunning").style.display="block";
        setTimeout(onStartGAN_sub, 10);
    }
}

async function onStartGAN_sub(){
    let ct = document.getElementById("dectgan_celltype").value;
    let a = parseInt(document.getElementById("epoch_start").value);
    let b = parseInt(document.getElementById("epoch_end").value);
    let c = parseInt(document.getElementById("epoch_term").value);
    await eel.startGAN(ct, a, b, c)();
    isRunning = false;
    document.getElementById("processrunning").style.display="none";
    document.getElementById("assess").classList.add("enable");
}

function onStartAssess(){
    if(!isRunning){
        isRunning = true;
        document.getElementById("processrunning").style.display="block";
        setTimeout(onStartAssess_sub, 10);
    }
}

//[lastrun, count, x_embedded.tolist()]
async function onStartAssess_sub(){
    const assess = await eel.assessGAN()();
    
    const datasets = [];

    let data = [];
    for(let i=0;i<assess[1][0];i++){
        data.push({x:assess[2][i][0],y:assess[2][i][1]});
    }
    datasets.push({label:assess[0][0],data:data});

    for(let i=1; i<assess[1].length;i++){
        data = [];
        for(let j=assess[1][i-1];j<assess[1][i];j++){
            data.push({x:assess[2][j][0],y:assess[2][j][1]});
        }
        datasets.push({label:"GAN"+assess[0][0] + (i-1)*assess[0][3],data:data});
    }
    const ctx = document.getElementById("scatter_2").getContext("2d");
    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: datasets,
        },
        options:{
            responsive:false,
        }
    });

    isRunning = false;
    document.getElementById("processrunning").style.display="none";
}
