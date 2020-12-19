<script>
import { Bar } from 'vue-chartjs'


export default {
  extends: Bar,
  props: ['data', 'labels', 'type', 'ymax'],
  data() {
    return {
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{
              ticks: {
                stepSize: this.type=='hr'? 10 : 100,
                min:0,
                suggestedMax: this.type=='hr'? 150 : 200
              }
          }]
        }
      }
    }
  },
  mounted () {
    this.renderChart({
      labels: this.labels,
      datasets: [
        {
          label: this.type=='hr'?'BPM':'Steps',
          backgroundColor: this.type=='hr'?'#f87979':'#5F9EA0',
          data: this.data
        }
      ],
    }, this.options)
  }
}
</script>