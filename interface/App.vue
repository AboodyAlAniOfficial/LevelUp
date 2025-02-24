<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Level Up</strong></router-link>

        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div class="navbar-menu" id="navbar-menu">
        <div class="navbar-end">
          <router-link to="/tracker" class="navbar-item">Daily Tracker</router-link>
          <router-link to="/leaderboard" class="navbar-item">Leaderboards</router-link>

          <div class="navbar-item">
            <div class="buttons">
              <!-- IMPLEMENT THE LOGIN/PROFILE BUTTON -->
              <!-- <template v-if="$store.state.isAuthenticated">
                <router-link to="/my-account" class="button is-light">My Account</router-link>
              </template>

              <template v-else>
                
              </template> -->
              <router-link to="/login" class="button is-light">Log In</router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <section class="section">
      <router-view/>
    </section>

    <footer class="footer">
      <p class="has-text-centered">EECS4314 Project - Group 6</p>
    </footer>
  </div>
</template>

<style lang="scss">
@import '../node_modules/bulma';
</style>
