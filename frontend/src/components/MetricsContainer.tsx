type MetricsContainerProps = {
    title: string;
    value: string;
}

function MetricsContainer({ title, value }: MetricsContainerProps) {
    return (
        <>
            <div className='metrics-container'>
                <div><h3 className='metrics-container-title'>{title}</h3></div>
                <h4 className='metrics-container-content'>{value}</h4>
            </div>
        </>
    )
}

export default MetricsContainer;
