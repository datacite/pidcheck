
class PIDMetadataPipeline():
    """Looks at scraped metadata to see what ID's match our known PID identifier"""
    def process_item(self, item, spider):
        item['pid_meta_match'] = []
        item['pid_meta_different'] = []

        # Look for a PID ID matches in schema org metadata
        for schema in item['schema_org']:
            id = schema.get('@id')

            # Check if the ID matches our known PID
            if id and item['pid'] in id:
                item['pid_meta_match'].append('schema_org')
            else:
                item['pid_meta_different'].append('schema_org')

        for id in item['dc_identifiers']:
            if item['pid'] in id:
                item['pid_meta_match'].append('dc.identifier')
            else:
                item['pid_meta_different'].append('dc.identifier')

        return item


class PIDScorePipeline():
    def process_item(self, item, spider):
        pass