import React from "react"
import ReactDOM from "react-dom"
import Autocomplete from "./AddressAutocomplete"; 
import GetLocation from "./GetLocation";

// CSS imports
import "@blueprintjs/core/lib/css/blueprint.css";
import "@blueprintjs/icons/lib/css/blueprint-icons.css";

ReactDOM.render(
  <React.StrictMode>
    <GetLocation />
  </React.StrictMode>,
  document.getElementById("root")
)
