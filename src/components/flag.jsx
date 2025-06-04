import {ReactSVG} from "react-svg";
import './flag.css'
import {useCallback, useEffect, useRef, useState} from "react";


export const Flag = ({countryCode, selectedColor}) => {
    const [flagComponents, setFlagComponents] = useState({});
    const selectedColorRef = useRef(selectedColor);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(true);
    }, [countryCode]);

    useEffect(() => {
        selectedColorRef.current = selectedColor;
    }, [selectedColor]);

    const componentClick = useCallback((svgElement, component, id, color) => {
        if (id) {
            svgElement.querySelectorAll('.flag-component').forEach(el => {
                if (el.getAttribute('id') === id) {
                    el.setAttribute('fill', selectedColorRef.current);
                    // el.setAttribute('stroke', selectedColorRef.current);
                }
            });
        } else {
            component.setAttribute('fill', selectedColorRef.current);
            // component.setAttribute('stroke', selectedColorRef.current);
        }
    }, []);

    const extractSvgData = (svgElement) => {
        const grays = [
            '#808080',
            '#909090',
            '#9D9D9D',
            '#A7A7A7',
        ]
        const newFlagComponents = {}
        const usedGreys = {}
        svgElement.querySelectorAll('.flag-component').forEach(el => {
            const color = el.getAttribute('fill');
            const id = el.getAttribute('id');
            if (id && newFlagComponents[id]) {
                newFlagComponents[id] = [{
                        el: el,
                        id: id,
                        color: color,
                    },
                    ...newFlagComponents[id]];
            } else {
                newFlagComponents[id] = [{
                    el: el,
                    id: id,
                    color: color,
                }]
            }
            if (id) {
                if (!usedGreys[id]) {
                    console.log(`Setting initial gray for ${id}`)
                    usedGreys[id] = grays.pop()
                }
                console.log(`reusing usedGreys[${id}] = ${usedGreys[id]}`)
                el.setAttribute('fill', usedGreys[id]);
                // el.setAttribute('stroke', usedGreys[id]);
            } else {
                const color = grays.pop()
                el.setAttribute('fill', color);
                // el.setAttribute('stroke', color);
            }
            el.addEventListener('click', (e) => {
                componentClick(svgElement, el, id, color);
            })
        })
        setFlagComponents(newFlagComponents)
        setLoading(false)
    }

    const loadFlag = useCallback(() => {
        const timeout = setTimeout(() => {
            const svgElement = document.querySelector("svg");
            if (svgElement) {
                extractSvgData(svgElement);
            }
        }, 100)
        return () => clearTimeout(timeout)
    }, [countryCode]);

    return (
        <div className="flag-container" hidden={loading}>
            <ReactSVG
                src={`flags/${countryCode}.svg`}
                afterInjection={loadFlag}
            />
        </div>
    )
}