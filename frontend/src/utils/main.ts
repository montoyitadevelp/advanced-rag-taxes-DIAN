export const formatTime = (date: Date) =>{
    return date.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' });
}
