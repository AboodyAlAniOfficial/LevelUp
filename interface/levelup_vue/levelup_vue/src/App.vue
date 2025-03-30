<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Level Up</strong></router-link>

        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active': showMobileMenu}">
        <div class="navbar-end">
          <router-link to="/about" class="navbar-item">About</router-link>

          <template v-if="activeUsername()">
          <div class="navbar-item" @click="isOpen = !isOpen">
            <button>Daily Trackers</button>
            <svg viewBox="0 0 1030 638" width="10">
              <path d="M1017 68L541 626q-11 12-26 12t-26-12L13 68Q-3 49 6 24.5T39 0h952q24 0 33 24.5t-7 43.5z" fill="#FFF"></path>
            </svg>
            <transition name="fade" appear>
              <div class="sub-menu" v-if="isOpen">
                <div>
                  <router-link class="navbar-item" to="/meal">Meal Tracker</router-link>
                  <router-link class="navbar-item" to="/exercise">Exercise Tracker</router-link>
                </div>
              </div>
            </transition>
          </div>

          <router-link to="/leaderboard" class="navbar-item">Leaderboards</router-link>

          <div class="navbar-item">
            <div class="buttons">
                <router-link to="/profile" class="button is-light">{{ activeUsername() }}</router-link>
                <button @click="logout">Log Out</button>
            </div>
          </div>
          </template>

          <template v-else>
            <router-link to="/login" class="button is-light">Log In or Sign Up</router-link>
          </template>
        </div>
      </div>
    </nav>

    <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
      <div class="lds-dual-ring"></div>
    </div>

    <section class="section">
      <router-view/>
    </section>

    <footer class="footer">
      <p class="has-text-centered">EECS4314 Project - Group 6</p>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showMobileMenu: false,
      isOpen: false,
    }
  },
  methods: {
    activeUsername() {
      return window.localStorage.getItem("active_username");
    },
    logout() {
      window.localStorage.removeItem("active_username");
      window.location.href = "/";
    }
  }
}
</script>

<style lang="scss">
@import '../node_modules/bulma';

nav .navbar-item svg {
  width: 10px;
}

nav .navbar-item .sub-menu {
  position: absolute;
  top: calc(100%);
  left: 50%;
  transform: translateX(-50%);
  width: max-content;
}

nav .sub-menu {
  background-color: rgb(46, 51, 61);
}

.fade-enter-active,
.fade-leave-active {
  transition: all .25s ease-out;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
