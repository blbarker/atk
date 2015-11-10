/**
 *  Copyright (c) 2015 Intel Corporation 
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

package org.trustedanalytics.atk.giraph.io;

import com.google.common.collect.Lists;
import org.apache.giraph.edge.Edge;
import org.apache.giraph.edge.EdgeFactory;
import org.apache.giraph.edge.OutEdges;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.junit.Test;

import java.util.List;

import static org.apache.giraph.graph.TestVertexAndEdges.instantiateOutEdges;
import static org.junit.Assert.assertEquals;

public class BigDataEdgesTest {

    @Test
    public void testBigDataEdges() {
        OutEdges<LongWritable, DoubleWritable> edges =
                instantiateOutEdges(BigDataEdges.class);

        // Initial edges list contains parallel edges.
        List<Edge<LongWritable, DoubleWritable>> initialEdges = Lists.newArrayList(
                EdgeFactory.create(new LongWritable(1), new DoubleWritable(1)),
                EdgeFactory.create(new LongWritable(2), new DoubleWritable(2)),
                EdgeFactory.create(new LongWritable(3), new DoubleWritable(3)),
                EdgeFactory.create(new LongWritable(2), new DoubleWritable(20)));

        edges.initialize(initialEdges);

        // The parallel edges should still be there.
        assertEquals(4, edges.size());

        // Adding a parallel edge should increase the number of edges.
        edges.add(EdgeFactory.create(new LongWritable(3), new DoubleWritable(30)));
        assertEquals(5, edges.size());

        // Removing edges pointing to a given vertex should remove all parallel
        // edges.
        edges.remove(new LongWritable(2));
        assertEquals(3, edges.size());
    }
}