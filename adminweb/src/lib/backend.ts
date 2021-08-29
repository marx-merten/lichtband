import {writable} from 'svelte/store'

class RGBWValue{
    constructor(readonly red:number,readonly green:number, readonlyblue:number, readonly white:number){}
}
class LightState{
    state = false
    rgbw=new RGBWValue(0,0,0,0)
    currentScene=""
    scenes:string[]
}

export const lightStats = writable(new LightState())
