
const CACHE = "ypf-vintage-v2";

const ARCHIVOS = [
  "./",
    "./index.html",
      "./manifest.json",
        "./icon-192.png",
          "./icon-512.png"
          ];

          self.addEventListener("install", evento => {
            evento.waitUntil(
                caches.open(CACHE).then(cache => {
                      return cache.addAll(ARCHIVOS);
                          })
                            );

                              self.skipWaiting();
                              });

                              self.addEventListener("activate", evento => {
                                evento.waitUntil(
                                    caches.keys().then(nombres => {
                                          return Promise.all(
                                                  nombres
                                                            .filter(nombre => nombre !== CACHE)
                                                                      .map(nombre => caches.delete(nombre))
                                                                            );
                                                                                }).then(() => self.clients.claim())
                                                                                  );
                                                                                  });

                                                                                  self.addEventListener("fetch", evento => {
                                                                                    if (evento.request.method !== "GET") return;

                                                                                      evento.respondWith(
                                                                                          fetch(evento.request).catch(() => {
                                                                                                return caches.match(evento.request);
                                                                                                    })
                                                                                                      );
                                                                                                      });
                                                                                                      