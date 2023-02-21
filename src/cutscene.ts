function loadCutscene(name: string) {
    $.ajax({
      url: `cutscenes/${name}.txt`,
      success: function (data){
        //parse your data here
        //you can split into lines using data.split('\n') 
        //an use regex functions to effectively parse it
        console.log(data)
      }
    });
  }