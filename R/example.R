library(starsim)
load_starsim()
phc <- import('phcsim')

do_plot <- TRUE

sim = phc$Sim(n_agents=10e3)
sim$run()
print(sim$results)
if (do_plot) {
    sim$plot()
}