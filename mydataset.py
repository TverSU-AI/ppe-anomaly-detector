#!/usr/bin/env python3

"""
   Copyright 2023 IQT Labs LLC

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import os

from anomaly import AnomalyDetector

print("lets get it started, ha")

kmeans_clusters_list = [3, 5, 7, 10, 15]
kmeans_neighbors_list = [1, 3]
pca_variance_list = [0.8, 0.9, 0.95, 0.99]
threshold_mode_list = ['cdf', 'zscore']
val_fraction_list = [0.2, 0.3]
val_not_generated_list = [False]

i = 0
start_from = [3, 1, 0.8, 'cdf', 0.2, False]
for kmeans_clusters in kmeans_clusters_list:
    for kmeans_neighbors in kmeans_neighbors_list:
        for pca_variance in pca_variance_list:
            for threshold_mode in threshold_mode_list:
                for val_fraction in val_fraction_list:
                    for val_not_generated in val_not_generated_list:
                        print(i + 1,
                              len(kmeans_clusters_list) *
                              len(kmeans_neighbors_list) *
                              len(pca_variance_list) *
                              len(threshold_mode_list) *
                              len(val_fraction_list) *
                              len(val_not_generated_list)
                              )
                        i += 1
                        if start_from is not None and [kmeans_clusters,
                                  kmeans_neighbors,
                                  pca_variance,
                                  threshold_mode,
                                  val_fraction,
                                  val_not_generated] != start_from:
                            continue
                        else:
                            start_from = None
                        ad = AnomalyDetector(
                            kmeans_clusters=kmeans_clusters,
                            kmeans_neighbors=kmeans_neighbors,
                            pca_variance=pca_variance,
                            threshold_mode=threshold_mode,
                            val_fraction=val_fraction,
                            verbose=1
                        )
                        ad.train('mydataset/train', 'mydataset/val' if val_not_generated else None)
                        # ad.save('mydataset/model.pickle')
                        output_path = f'mydataset/t/output{i}'
                        try:
                            os.mkdir(output_path)
                        except FileExistsError:
                            pass

                        with open(os.path.join(output_path, 'params.txt'), 'w') as out:
                            print(kmeans_clusters,
                                  kmeans_neighbors,
                                  pca_variance,
                                  threshold_mode,
                                  val_fraction,
                                  val_not_generated,
                                  file=out)

                        # ad = AnomalyDetector.load('mydataset/model.pickle')
                        ad.test('mydataset/test', output_path)
