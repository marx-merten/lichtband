import { derived, readable, writable } from 'svelte/store'
import { fetch_api,put_file } from '$lib/servercalls'
import { space } from 'svelte/internal';

class WifiConfig {
    constructor(public ssid: string, public password: string) { }

}

class MQTTConfig {
    constructor(public server: string,
        public port: number, public prefix: string,
        public online: string, public name: string) { }

}

class LedConfig {
    constructor(public count: number) { }
}

class Config {

    network: WifiConfig = new WifiConfig("","");
    mqtt: MQTTConfig = new MQTTConfig("",1883,"","","");
    led: LedConfig = new LedConfig(100);

    public static fromDO(data): Config {
        const cfg = new Config()
        if (data) {
            cfg.network = new WifiConfig(data.network.ssid, data.network.password);
            cfg.mqtt = new MQTTConfig(data.mqtt.server, data.mqtt.port, data.mqtt.prefix, data.mqtt.online, data.mqtt.name)
            cfg.led = new LedConfig(data.led.count)
        }
        return cfg;
    }
    public toJson():string{
        return JSON.stringify(this,null,4);
    }
}

let lastLoadedConfig=""
export const iotConfig = writable(new Config())
export const iotConfigChanged=writable(false)


iotConfig.subscribe((val)=>{
    iotConfigChanged.set(val.toJson() !== lastLoadedConfig)
})


export async function fetch_cfg(): Promise<void> {
    await fetch_api('api/fs/file/cfg.json').then((cfg: any) => {
            const c= Config.fromDO(cfg)
            lastLoadedConfig=c.toJson()
            iotConfig.set(c)
        });
}

export async function store_cfg(cfg:Config): Promise<void> {
    lastLoadedConfig=cfg.toJson()
    await put_file("cfg.json", lastLoadedConfig)
    iotConfigChanged.set(false)
}

fetch_cfg()
