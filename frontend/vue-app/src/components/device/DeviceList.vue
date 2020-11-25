<template>
  <div>
    <b-card>
        <b-table striped hover :items="items"></b-table>
    </b-card>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        items: [
          { no: 1, MAC_address: 'Dickerson', authenctic_key: 'Macdonald', edit: '✏️', unpair: '❌'},
          { no: 2, MAC_address: 'Larsen', authenctic_key: 'Shaw', edit: '✏️', unpair: '❌' },
          { no: 3, MAC_address: 'Geneva', authenctic_key: 'Wilson', edit: '✏️', unpair: '❌' },
          { no: 4, MAC_address: 'Jami', authenctic_key: 'Carney', edit: '✏️', unpair: '❌' }
        ]
      }
    }
  }
</script>