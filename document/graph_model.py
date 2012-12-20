from matplotlib import rc
rc("font", family="serif", size=16)
rc("text", usetex=True)

import daft
pgm = daft.PGM([8, 6.75], origin=[0.5, 0.5], grid_unit=4., node_unit=2.0)
# Start with the plates.
tweak=0.02
rect_params = {"lw": 2}
pgm.add_plate(daft.Plate([1.5+tweak, 1.5+tweak, 6.0-2*tweak, 3.75-2*tweak], label=r"Planets N", rect_params=rect_params))


#   Bottom Row
asp = 1
pgm.add_node(daft.Node("tobs", r"$\Delta t_{obs}$", 6.0, 2.0, observed=True, aspect=asp))
pgm.add_node(daft.Node("fobs", r"$\Delta f_{obs}$", 3.0, 2.0, observed=True, aspect=asp))
pgm.add_node(daft.Node("q", r"$\mathrm{obs}$", 4.5, 2.5, observed=True, aspect=asp))


#  Second to the bottom
pgm.add_node(daft.Node("T", r"$T$", 3.2, 3.6, observed=True, aspect=asp))
pgm.add_node(daft.Node("Delf", r"$\Delta f / f$", 4.5, 3.6, observed=False, aspect=asp))
pgm.add_node(daft.Node("Delt", r"$\Delta t$", 5.8, 3.6, observed=False, aspect=asp))

#  Second to the Top
pgm.add_node(daft.Node("Star", r"$\star$", 2.6, 4.5, observed=False, aspect=asp))
pgm.add_node(daft.Node("a", r"$a$", 3.9, 4.5, observed=False, aspect=asp))
pgm.add_node(daft.Node("Deltai", r"$\Delta i$", 5.2, 4.5, observed=False, aspect=asp))
pgm.add_node(daft.Node("r", r"$r$", 6.5, 4.5, observed=False, aspect=asp))

#   Top Row
pgm.add_node(daft.Node("Gamma", r"$\Gamma_*$", 2.6, 6.0, observed=False, aspect=asp))
pgm.add_node(daft.Node("thetaa", r"$\theta_a$", 3.9, 6.0, observed=False, aspect=asp))
pgm.add_node(daft.Node("thetadel", r"$\theta_{\Delta i}$ ", 5.2, 6.0, observed=False, aspect=asp))
pgm.add_node(daft.Node("thetar", r"$\theta_r$", 6.5, 6.0, observed=False, aspect=asp))

#  Off to the side
pgm.add_node(daft.Node("S", r"$S$", 8.0, 2.5, observed=False, aspect=asp))

pgm.add_edge("Gamma","Star")
pgm.add_edge("thetaa","a")
pgm.add_edge("thetadel","Deltai")
pgm.add_edge("thetar","r")
pgm.add_edge("Star","T")
pgm.add_edge("Star","Delf")
pgm.add_edge("Star","Delt")
pgm.add_edge("a","T")
pgm.add_edge("a","Delf")
pgm.add_edge("a","Delt")
pgm.add_edge("Deltai","Delf")
pgm.add_edge("Deltai","Delt")
pgm.add_edge("r","Delt")
pgm.add_edge("r","Delf")
pgm.add_edge("Delf","fobs")
pgm.add_edge("Delf","q")
pgm.add_edge("Delt","q")
pgm.add_edge("Delt","tobs")
pgm.add_edge("S","q")



  # Render and save.
pgm.render()
pgm.figure.savefig("graph_model.pdf")
pgm.figure.savefig("graph_model.png", dpi=150)
