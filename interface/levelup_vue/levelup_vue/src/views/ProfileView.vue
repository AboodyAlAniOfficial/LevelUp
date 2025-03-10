<template>
    <div class="column is-multiline">
        <label for="lengthselect">Length Unit: </label>
        <select id="lengthselect" name="length" @change="updateUnits">
            <option value="m">Metre (m)</option>
            <option value="cm">Centimetre (cm)</option>
            <option value="mm">Millimetre (mm)</option>
            <option value="ft">Foot (’)</option>
        </select>

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
     console.log("hi");
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
       console.log("changed - " + this.getLengthUnit());
       for (const [id, value] of LENGTH_VALUES) {
         console.log(id, value);
         document.getElementById(id).innerText =
           this.getUnitValue("length", value) + " " + this.getLengthUnit();
       }
     }
   }
}
</script>
