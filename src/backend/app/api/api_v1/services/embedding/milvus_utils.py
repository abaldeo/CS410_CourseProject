from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from pymilvus.client.types import MetricType, IndexType
from loguru import logger

#TODO WIP 
class MilvusDBUtils:
    def __init__(self, host, port, user, passwd) -> None:
        logger.info(f"\nCreate connection...")
        connections.connect(host=host, port=port, user=user, password=passwd)
        logger.info(f"\nList connections:")
        logger.info(connections.list_connections())

    
    
    def create_collection(self, collection_name: str, 
                          dimension: int, 
                          index_file_size: int = 1024,
                          metric_type: str = MetricType.COSINE) -> None:
        """Creates a collection in MilvusDB."""
        try:
            status = utility.has_collection(collection_name)
            if not status.ok:
                utility.create_collection({
                    "collection_name": collection_name,
                    "dimension": dimension,
                    "index_file_size": index_file_size,
                    "metric_type": metric_type
                })
        except Exception as e:
            logger.error(e)
            raise e                    
        
    def list_parititions(self, collection_name: str) -> List[str]:
        """Returns a list of partitions for a collection."""
        try:
            partitions = client.list_partitions(collection_name)
            return partitions
        except Exception as e:
            logger.error(e)
            raise e
        
    def create_partitions(self, collection_name: str, partitions: List[str]) -> None:
        """Creates partitions for a collection."""
        try:
            for partition_name in partitions:
                status = utility.has_partition(collection_name, partition_name)
                if not status.ok:
                    utility.create_partition(collection_name, partition_name)
        except Exception as e:
            logger.error(e)
            raise e

    def get_collection_stats(self, collection_name: str) -> dict:
        """Returns a dictionary of collection stats."""
        try:
            stats = client.get_collection_stats(collection_name)
            return stats
        except Exception as e:
            logger.error(e)
            raise e
        
    def show_collection_stats(self, collection_name: str) -> None:  
        """Prints collection stats."""
        stats = self.get_collection_stats(collection_name)
        logger.info(stats)
 
    def get_collection_row_count(self, collection_name: str) -> int:
        """Returns the number of entities in a collection."""
        stats = self.get_collection_stats(collection_name)
        num_entities = stats["row_count"]
        return num_entities

    def get_rows(self, collection_name: str, ids: List[int]) -> dict:
        """Returns a dictionary of row info."""
        try:
            row_info = client.get_entity_by_id(collection_name, ids)
            return row_info
        except Exception as e:
            logger.error(e)
            raise e

    def delete_rows_by_id(self, collection_name: str, ids: List[int]) -> None:
        """Deletes entities from a collection."""
        try:
            client.delete_entity_by_id(collection_name, ids)
        except Exception as e:
            logger.error(e)
            raise e
    
    def drop_paritions(self, collection_name: str, partitions: List[str]) -> None:
        """Drops partitions from a collection."""
        try:
            for partition_name in partitions:
                logger.warn(f"Dropping partiton: {partition_name} ")   
                collection= Collection(collection_name)             
                collection.drop_partition( partition_name)
        except Exception as e:
            logger.error(e)
            raise e

    def drop_collection(self, collection_names: List[str]) -> None:
        """Drops collections."""
        try:
            for collection_name in collection_names:
                logger.warn(f"Dropping collection: {collection_name}")                
                utility.drop_collection(collection_name)
        except Exception as e:
            logger.error(e)
            raise e

    def rename_collection(self, old_collection_names: List[str], new_collection_names: List[str]) -> None:
        """Renames collections."""
        if not isinstance(old_collection_names, list):
            old_collection_names = [old_collection_names]
        if not isinstance(new_collection_names, list):
            new_collection_names = [new_collection_names]
        if len(old_collection_names) != len(new_collection_names):
            raise ValueError("old_collection_names and new_collection_names must be the same length")
        try:
            for old_name, new_name in zip(old_collection_names, new_collection_names):
                logger.warn(f"Renaming collection: {old_name} to {new_name}")                
                utility.rename_collection(old_name, new_name)
        except Exception as e:
            logger.error(e)
            raise e

    # def insert_data(self, number: int):
    #     print(fmt.format(f"No.{number:2}: Start inserting entities"))
    #     rng = np.random.default_rng(seed=number)
    #     entities = [
    #         list(range(num_entities)),
    #         rng.random(num_entities).tolist(),
    #         rng.random((num_entities, dim)),
    #     ]

    #     insert_result = hello_milvus.insert(entities)
    #     assert len(insert_result.primary_keys) == num_entities
    #     print(fmt.format(f"No.{number:2}: Finish inserting entities"))

    # def insert_all_batches(self):
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    #         executor.map(self.insert_data, self.batchs)

    def __del__(self):
        for connection in connections.list_connections():
            logger.info(f"\nDisconnect connection: {connection}")
            connections.remove(connection)
        logger.debug(f"\nList connections:")
        logger.debug(connections.list_connections())


    def create_index(self, collection_name, field_name, 
                     Index_Type = IndexType.IVF_FLAT,
                     nlist = 16384,
                     MetricType = MetricType.L2,):
        index_param = {
            "index_type": Index_Type,
            "params": {"nlist": nlist},
            "metric_type": MetricType,
        }
        collection = Collection(collection_name)
        # if collection.has_index():
        #     logger.info("\nIndex already exists:\n{}\n Please drop it first.".format(collection.index().params))
        #     return
        # else:
        collection.create_index(field_name, index_param)
        utility.wait_for_index_building_complete(collection.name)
    
        logger.info("\nCreated index:\n{}".format(collection.index().params))


    def drop_index(self, collection_name):
        collection = Collection(collection_name)
        if collection.has_index():
            collection.drop_index()
            logger.info("\nDrop index sucessfully")
        else:
            logger.info("\nIndex doesn't exist")

        