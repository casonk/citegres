"""
Tests for citegres.netility — graph construction, metrics, and layout utilities.
All tests operate on in-memory graphs; no database or network access required.
"""

from unittest.mock import patch

import networkx as nx
import pandas as pd
import pytest

import netility

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def simple_directed_graph():
    G = nx.DiGraph()
    G.add_weighted_edges_from([("A", "B", 2), ("B", "C", 1), ("A", "C", 3)])
    return G


@pytest.fixture()
def edge_df():
    """Two-column DataFrame representing citation pairs."""
    return pd.DataFrame({"source": ["A", "A", "B", "A"], "target": ["B", "C", "C", "B"]})


# ---------------------------------------------------------------------------
# construct_graph_from_df
# ---------------------------------------------------------------------------


class TestConstructGraphFromDf:
    def test_directed_returns_digraph(self, edge_df):
        G = netility.construct_graph_from_df(edge_df, directed=True)
        assert isinstance(G, nx.DiGraph)

    def test_undirected_returns_graph(self, edge_df):
        G = netility.construct_graph_from_df(edge_df, directed=False)
        assert isinstance(G, nx.Graph)
        assert not isinstance(G, nx.DiGraph)

    def test_nodes_present(self, edge_df):
        G = netility.construct_graph_from_df(edge_df)
        assert set(G.nodes()) == {"A", "B", "C"}

    def test_edges_weighted(self, edge_df):
        G = netility.construct_graph_from_df(edge_df)
        # A->B appears twice so weight should be 2
        assert G["A"]["B"]["weight"] == 2

    def test_single_edge(self):
        df = pd.DataFrame({"src": ["X"], "dst": ["Y"]})
        G = netility.construct_graph_from_df(df)
        assert G.number_of_edges() == 1

    def test_empty_df_produces_empty_graph(self):
        df = pd.DataFrame({"src": [], "dst": []})
        G = netility.construct_graph_from_df(df)
        assert G.number_of_nodes() == 0
        assert G.number_of_edges() == 0


# ---------------------------------------------------------------------------
# construct_static_layout
# ---------------------------------------------------------------------------


class TestConstructStaticLayout:
    LAYOUTS = [
        "spring",
        "fruchterman_reingold",
        "planar",
        "shell",
        "random",
        "circular",
    ]

    @pytest.mark.parametrize("layout", LAYOUTS)
    def test_layout_returns_dict(self, simple_directed_graph, layout):
        pos = netility.construct_static_layout(simple_directed_graph, layout=layout)
        assert isinstance(pos, dict)

    def test_spring_default_returns_all_nodes(self, simple_directed_graph):
        pos = netility.construct_static_layout(simple_directed_graph)
        assert set(pos.keys()) == set(simple_directed_graph.nodes())

    def test_position_values_are_2d(self, simple_directed_graph):
        pos = netility.construct_static_layout(simple_directed_graph, layout="circular")
        for coords in pos.values():
            assert len(coords) == 2

    def test_spiral_layout_returns_callable(self, simple_directed_graph):
        # spiral branch returns the layout function object, not a dict
        result = netility.construct_static_layout(simple_directed_graph, layout="spiral")
        assert callable(result)

    def test_spectral_layout(self, simple_directed_graph):
        pos = netility.construct_static_layout(simple_directed_graph, layout="spectral")
        assert isinstance(pos, dict)


# ---------------------------------------------------------------------------
# compute_graph_metrics
# ---------------------------------------------------------------------------


class TestComputeGraphMetrics:
    def test_default_returns_betweenness(self, simple_directed_graph):
        metrics = netility.compute_graph_metrics(simple_directed_graph)
        assert "betweenness_centralities" in metrics
        assert len(metrics["betweenness_centralities"]) == simple_directed_graph.number_of_nodes()

    def test_in_degrees(self, simple_directed_graph):
        metrics = netility.compute_graph_metrics(simple_directed_graph, in_degrees=True)
        assert "in_degrees" in metrics
        assert len(metrics["in_degrees"]) == simple_directed_graph.number_of_nodes()

    def test_out_degrees(self, simple_directed_graph):
        metrics = netility.compute_graph_metrics(
            simple_directed_graph,
            out_degrees=True,
            in_degrees=False,
            betweenness_centralities=False,
        )
        assert "out_degrees" in metrics

    def test_degree_centralities(self, simple_directed_graph):
        metrics = netility.compute_graph_metrics(
            simple_directed_graph,
            degree_centralities=True,
            betweenness_centralities=False,
        )
        assert "degree_centralities" in metrics

    def test_closeness_centralities(self, simple_directed_graph):
        metrics = netility.compute_graph_metrics(
            simple_directed_graph,
            closeness_centralities=True,
            betweenness_centralities=False,
        )
        assert "closeness_centralities" in metrics

    def test_all_metrics_disabled_returns_empty(self, simple_directed_graph):
        metrics = netility.compute_graph_metrics(
            simple_directed_graph,
            degrees=False,
            out_degrees=False,
            in_degrees=False,
            degree_centralities=False,
            closeness_centralities=False,
            betweenness_centralities=False,
        )
        assert metrics == {}

    def test_betweenness_values_in_range(self, simple_directed_graph):
        metrics = netility.compute_graph_metrics(simple_directed_graph)
        for val in metrics["betweenness_centralities"]:
            assert 0.0 <= val <= 1.0

    def test_single_node_graph(self):
        G = nx.DiGraph()
        G.add_node("solo")
        metrics = netility.compute_graph_metrics(G)
        assert metrics["betweenness_centralities"] == [0.0]


# ---------------------------------------------------------------------------
# plot_graph (side-effect mocked — no display)
# ---------------------------------------------------------------------------


class TestPlotGraph:
    def test_plot_graph_calls_show(self, simple_directed_graph):
        pos = netility.construct_static_layout(simple_directed_graph, layout="circular")
        with patch("netility.plt.show") as mock_show, patch("netility.plt.figure"):
            netility.plot_graph(
                simple_directed_graph,
                pos=pos,
                use_labels=True,
                alpha=0.8,
                edge_color="white",
                width=1.0,
                arrowsize=10,
                node_size=300,
                node_color="blue",
                cmap="rainbow",
            )
            mock_show.assert_called_once()

    def test_plot_graph_rainbow_cmap_resolved(self, simple_directed_graph):
        """rainbow string should be resolved to plt.cm.rainbow before draw."""
        import matplotlib.pyplot as mpl_plt

        pos = netility.construct_static_layout(simple_directed_graph, layout="circular")
        with (
            patch("netility.plt.show"),
            patch("netility.plt.figure"),
            patch("netility.nx.draw_networkx") as mock_draw,
        ):
            netility.plot_graph(
                simple_directed_graph,
                pos=pos,
                use_labels=False,
                alpha=1.0,
                edge_color="gray",
                width=1.0,
                arrowsize=5,
                node_size=100,
                node_color="red",
                cmap="rainbow",
            )
            _, kwargs = mock_draw.call_args
            assert kwargs["cmap"] == mpl_plt.cm.rainbow


# ---------------------------------------------------------------------------
# POS_LAYOUT constant
# ---------------------------------------------------------------------------


def test_pos_layout_default():
    assert netility.POS_LAYOUT == "spring"
