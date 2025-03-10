<template>
    <div class="column is-multiline">
        <label for="lengthselect">Length Unit: </label>
        <select id="lengthselect" name="length" @change="updateUnits">
            <option value="m">Metre (m)</option>
            <option value="cm">Centimetre (cm)</option>
            <option value="mm">Millimetre (mm)</option>
            <option value="ft">Foot (’)</option>
        </select>
        <br>
        <button @click="saveUnits" class="button is-dark">Save Units</button>
        <br>

        <p>Example values:</p>
        <ul>
            <li>Average Canadian height:
                <span id="height"></span>
            </li>
        </ul>
    </div>
</template>

<script>
 import axios from 'axios';

 // sizes of available units
 const LENGTH_UNITS = new Map();
 LENGTH_UNITS.set("m", 1.0);
 LENGTH_UNITS.set("cm", 1e-2);
 LENGTH_UNITS.set("mm", 1e-3);
 LENGTH_UNITS.set("ft", 0.3048);

 // values to set
 const LENGTH_VALUES = new Map();
 // id 'height' will be set to 1.7 m or equivalent in other unit
 LENGTH_VALUES.set("height", 1.7);

 export default {
   name: 'ProfileView',
   data() {
     return {
       userProfile: []
     }
   },
   mounted() {
     // this.getUserProfile();
     this.loadUnits();
     this.updateUnits();
   },
   methods: {
     getUserProfile() { //STUB: Need to update to match component app in django
       axios
       .get('api/v1/u/profile') //Name of the django page storing these data
       .then(response=>{
         this.profile = response.data
       })
       .catch(error=>{
         console.log(error)
       })
     },
     getLengthUnit() {
       return document.getElementById("lengthselect").value;
     },
     getUnitValue(dimension, value) {
       if (dimension == "length") {
         const unit = this.getLengthUnit();
         return (value / LENGTH_UNITS.get(unit)).toPrecision(4);
       }
     },
     updateUnits() {
       for (const [id, value] of LENGTH_VALUES) {
         document.getElementById(id).innerText =
           this.getUnitValue("length", value) + " " + this.getLengthUnit();
       }
     },
     loadUnits() {
       const xhr = new XMLHttpRequest();
       xhr.addEventListener("load", function(evt) {
         if (xhr.response != "No units set for this user.") {
           document.getElementById("lengthselect").value = xhr.response;
         }
       });
       const url = `http://localhost:8000/accounts/unit/?username=${localStorage.getItem("active_username")}&dimension=length`
       xhr.open("GET", url, false);
       xhr.send();
     },
     saveUnits() {
       const xhr = new XMLHttpRequest();
       const url = "http://localhost:8000/accounts/unit/"
       xhr.open("POST", url, false);
       const form_data = new FormData();
       form_data.append('username', localStorage.getItem("active_username"));
       form_data.append('dimension', 'length');
       form_data.append('unitname',
                        document.getElementById("lengthselect").value);
       xhr.send(form_data);
     }
   }
}
</script>
