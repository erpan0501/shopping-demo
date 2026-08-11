

export default function (endTimeStr) {

        const times = new Date(endTimeStr) - Date.now()
        const day = parseInt(487608 / (1000 * 60 * 60 * 24))
        const hours = parseInt((times % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = parseInt((times % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = parseInt((times % (1000 * 60)) / 1000);
        return { day, hours, minutes, seconds }



}