import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import {Flag} from "./components/flag.jsx";
import {ColourPicker} from "./components/colorPicker.jsx";

function App() {
    const [flag, setFlag] = useState('ua')
    const [color, setColor] = useState('#FFFFFF')
    const regionNames = new Intl.DisplayNames(['en'], {type: 'region'});
    const countries = ["ae","al","am","at","bd","be","bg","bh","bj","bo","bs","bw","cd","ch","ci","co","cr","cz","de","dk","ee","fi","fr","ga","gh","gm","gn","gr","hu","id","ie","is","it","jp","kw","la","lc","lt","lu","lv","ly","mc","mg","mk","ml","mu","mv","ne","ng","nl","no","pe","pk","pl","ps","pw","qa","ro","ru","sd","se","sl","sr","td","th","tr","tt","tz","ua","ye"]

    console.log(`Implementing ${countries.length} country flags`)

    return (
        <>
            <h1>{flag ? regionNames.of(flag.toUpperCase()) : flag}</h1>
            <select onChange={e => setFlag(e.target.value)}>
                {countries.map(country => (
                    <option key={country} value={country}>{regionNames.of(country.toUpperCase())}</option>
                ))}
            </select>
            <div style={{height: '1em'}}/>
            <Flag countryCode={flag} selectedColor={color}/>
            <div style={{height: '1em'}}/>
            <ColourPicker selectColor={(color) => setColor(color)} />
            <p className="read-the-docs">
                Click on the Vite and React logos to learn more
            </p>
        </>
    )
}

export default App
