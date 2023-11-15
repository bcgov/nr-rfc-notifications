# Intro

A bunch of notes re: things that I have figured out w/ Chefs.

## Access Select component 'Raw Json'

``` 
var comp = component.data.json;
```



## Example dependency logic for component visibility

The following depends on a data struct from a component different from the component that is being used.

``` javascript
// extract the data component from the form
var dataComp = utils.getComponent(components=form.components, key="hiddenSelectData")

// get basin list from the data component
var basinList = Object.keys(dataComp.data.json)

// get the currently selected basin
currentBasin =  data.basin;

show = false;
if (basinList.includes(currentBasin)) {
  // now see if there are actually any sub basins for this basin
  var subBasinList = dataComp.data.json[currentBasin];
  console.log("sub basin list: " + JSON.stringify(subBasinList));
  
  if (subBasinList.length > 0) {
    // if there are sub basins for the current basin then show the subbasin
    // component
    show = true;
  }
}
```