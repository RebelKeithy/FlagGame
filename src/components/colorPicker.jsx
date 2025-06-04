import './colorPicker.css'
import {useEffect, useState} from "react";

export const ColourPicker = ({selectColor}) => {
    const [selectedColor, setSelectedColor] = useState(null)

    useEffect(() => {
        selectColor(selectedColor)
    }, [selectedColor])

    const colour = (color) => {
        return (<div
            className={`colourPicker__colour ${color === selectedColor ? 'selected' : ''}`}
            style={{backgroundColor: color}}
            onClick={() => setSelectedColor(color)}
        />)
    }

    return <div className="colourPicker">
        {colour('#000000')}
        {colour('#FFFFFF')}
        {colour('#C8102E')}
        {colour('#FFCD00')}
        {colour('#ABCAE9')}
        {colour('#003DA5')}
        {colour('#1B7339')}
    </div>
}